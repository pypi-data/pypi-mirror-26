from __future__ import absolute_import
from ctypes import addressof, byref, cast, c_char, c_void_p, pointer
import os
from struct import pack, unpack
from . import libaio
from .eventfd import eventfd, EFD_CLOEXEC, EFD_NONBLOCK, EFD_SEMAPHORE

__all__ = (
    'EFD_CLOEXEC', 'EFD_NONBLOCK', 'EFD_SEMAPHORE',
    'EventFD', 'AIOBlock', 'AIOContext',
    'AIOBLOCK_MODE_READ', 'AIOBLOCK_MODE_WRITE',
)

class EventFD(object):
    """
    Minimal file-like object for eventfd.
    """
    def __init__(self, initval, flags):
        """
        initval (int 0..2**64 - 1)
            Internal counter value.
        flags (int)
            Bit mask of EFD_* constants.
        """
        self._file = os.fdopen(eventfd.eventfd(initval, flags), 'r+b')

    def read(self):
        """
        Read current counter value.

        See manpage for flags effect on this.
        """
        return unpack('Q', self._file.read(8))[0]

    def write(self, value):
        """
        Add givel value to counter.
        """
        self._file.write(pack('Q', value))

    def fileno(self):
        """
        Return eventfd's file descriptor.
        """
        return self._file.fileno()

AIOBLOCK_MODE_READ = object()
AIOBLOCK_MODE_WRITE = object()

_AIOBLOCK_MODE_DICT = {
    AIOBLOCK_MODE_READ: libaio.IO_CMD_PREADV,
    AIOBLOCK_MODE_WRITE: libaio.IO_CMD_PWRITEV,
}

class AIOBlock(object):
    """
    Asynchronous I/O block.

    Defines a (list of) buffer(s) to read into or write from, and what should
    happen on completion.
    """
    def __init__(self, mode, target_file, buffer_list, offset, callback=None, eventfd=None):
        """
        mode (AIOBLOCK_MODE_READ or AIOBLOCK_MODE_WRITE)
            Whether data should be read into given buffers, or written from
            them.
        target_file (file-ish)
            The file to read from/write to.
        buffer_list (list of bytearray)
            Buffers to use.
        offset (int)
            Where to start reading from/writing to.
        callback
            XXX: not tested !
        eventfd (EventFD)
            An eventfd file, so AIO completion can be waited upon by
            select/poll/epoll.
        """
        self._iocb = iocb = libaio.iocb()
        self._iocb_ref = byref(iocb)
        self._file = target_file
        self._offset = offset
        self._buffer_list = buffer_list
        self._iovec = (libaio.iovec * len(buffer_list))(*[
            libaio.iovec(
                cast((c_char * len(x)).from_buffer(x), c_void_p),
                len(x),
            )
            for x in buffer_list
        ])
        self._callback = callback
        self._eventfd = eventfd
        libaio.zero(iocb)
        iocb.aio_fildes = target_file.fileno()
        iocb.aio_lio_opcode = _AIOBLOCK_MODE_DICT[mode]
        iocb.aio_reqprio = 0
        iocb.u.c.buf = cast(self._iovec, c_void_p)
        iocb.u.c.nbytes = len(buffer_list)
        iocb.u.c.offset = offset
        if callback is not None:
            libaio.io_set_callback(iocb, callback)
        if eventfd is not None:
            libaio.io_set_eventfd(iocb, eventfd)

    @property
    def iocb(self):
        """
        For internal use only.
        """
        return self._iocb

    @property
    def target_file(self):
        """
        The file object given to constructor.
        """
        return self._file

    @property
    def buffer_list(self):
        """
        The buffer list given to constructor.
        """
        return self._buffer_list

    @property
    def offset(self):
        """
        The offset given to constructor.
        """
        return self._offset

class AIOContext(object):
    """
    Linux Ashynchronous IO context.
    """
    def __init__(self, maxevents):
        """
        maxevents (int)
            Maximum number of events this context will have to handle.
        """
        self._maxevents = maxevents
        self._ctx = libaio.io_context_t()
        self._submitted = {}

    def open(self):
        """
        Initialises AIO context.
        """
        # Note: almost same as io_setup
        libaio.io_queue_init(self._maxevents, byref(self._ctx))

    def close(self):
        """
        Cancels all pending IO blocks.
        Waits until all non-cancellable IO blocks finish.
        De-initialises AIO context.
        """
        # Note: same as io_destroy
        libaio.io_queue_release(self._ctx)

    def __enter__(self):
        """
        Calls open() and returns self.
        """
        self.open()
        return self

    def __exit__(self, exc_type, ex_val, exc_tb):
        """
        Calls close.
        """
        self.close()

    def submit(self, block_list):
        """
        Submits transfers.

        block_list (list of AIOBlock)
            The IO blocks to hand off to kernel.
        """
        # XXX: if submit fails, we will have some blocks in self._submitted
        # which are not actually submitted.
        for block in block_list:
            self._submitted[addressof(block.iocb)] = block
        libaio.io_submit(
            self._ctx,
            len(block_list),
            (libaio.iocb_p * len(block_list))(*[
                pointer(x.iocb)
                for x in block_list
            ]),
        )

    def _eventToPython(self, event):
        return (
            self._submitted.pop(addressof(event.obj.contents)),
            event.res,
            event.res2,
        )

    def cancel(self, block):
        """
        Cancel an IO block.

        block (AIOBlock)
            The IO block to cancel.

        Returns cancelled block's event data.
        """
        event = libaio.io_event()
        libaio.io_cancel(self._ctx, block.iocb, event)
        return self._eventToPython(event)

    def getEvents(self, min_nr=1, nr=None, timeout=None):
        """
        Returns a list of event data from submitted IO blocks.

        min_nr (int)
            When blocking, minimum number of events to collect before
            returning.
        nr (int, None)
            Maximum number of events to return.
            If None, set to maxevents given at construction.
        timeout (float, None):
            Time to wait for events.
            If None, become blocking.
        """
        if nr is None:
            nr = self._maxevents
        if timeout is None:
            timeoutp = None
        else:
            sec = int(timeout)
            timeout = libaio.timespec(sec, int((timeout - sec) * 1e9))
            timeoutp = byref(timeout)
        event_buffer = (libaio.io_event * nr)()
        actual_nr = libaio.io_getevents(
            self._ctx,
            min_nr,
            nr,
            event_buffer,
            timeoutp,
        )
        return [
            self._eventToPython(event_buffer[x])
            for x in xrange(actual_nr)
        ]
