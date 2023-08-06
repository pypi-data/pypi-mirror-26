"""Boilerplate for asyncio applications"""
import logging
import asyncio
from asyncio import (
    get_event_loop,
    AbstractEventLoop,
    Task,
    gather,
    CancelledError,
    Future,
    sleep
)
from concurrent.futures import Executor, ThreadPoolExecutor
from signal import SIGTERM, SIGINT
from typing import Optional, Coroutine, Callable, Set
from weakref import WeakSet
from functools import partial


__all__ = ['run', 'shutdown_waits_for']
__version__ = '2017.10.4'
logger = logging.getLogger('aiorun')


_DO_NOT_CANCEL_COROS = WeakSet()


def shutdown_waits_for(coro, loop=None):
    """Prevent coro from being cancelled during the shutdown sequence.

    The trick here is that we add this coro to the global
    "DO_NOT_CANCEL" collection, and then later during the shutdown
    sequence we make sure that the task that wraps this coro will NOT
    be cancelled.

    To make this work, we have to create a super-secret task, below, that
    communicates with the caller (which "awaits" us) via a Future. Using
    a Future in this way allows us to avoid awaiting the Task, which
    decouples the Task from the normal exception propagation which would
    normally happen when the outer Task gets cancelled.  We get the
    result of coro back to the caller via Future.set_result.

    NOTE that during the shutdown sequence, the caller WILL NOT be able
    to receive a result, since the caller will likely have been
    cancelled.  So you should probably not rely on capturing results
    via this function.
    """
    loop = loop or get_event_loop()
    fut = Future(loop=loop)  # This future will connect coro and the caller.

    async def coro_proxy():
        """This function will await coro, but it will also send the result
        over the the future. Rememeber: the outside caller (of
        shutdown_waits_for) will be awaiting fut, NOT coro(), due to
        the decoupling. However, when coro completes, we need to send its
        result over to the fut to make it look *as if* it was just coro
        running the whole time. This whole thing is a teeny magic trick.
        """
        try:
            result = await coro
            try:
                fut.set_result(result)
            except asyncio.InvalidStateError:
                logger.warning('Failed to set result.')
        except CancelledError as e:
            fut.set_exception(e)

    new_coro = coro_proxy()  # We'll taskify this one instead of coro.
    _DO_NOT_CANCEL_COROS.add(new_coro)  # The new task must not be cancelled.
    loop.create_task(new_coro)  # Make the task

    # Ok, so we *could* simply return fut.  Callers can await it as normal,
    # e.g.
    #
    # async def blah():
    #   x = await shutdown_waits_for(bleh())
    #
    # That will work fine.  However, callers may *also* want to detach the
    # call from the current execution context, e.g.
    #
    # async def blah():
    #   loop.create_task(shutdown_waits_for(bleh()))
    #
    # This will only work if shutdown_waits_for() returns a coroutine.
    # Therefore, we just make a new coroutine to wrap the `await fut` and
    # return that.  Then both things will work.
    #
    # (Side note: instead of callers using create_tasks, it would also work
    # if they used `asyncio.ensure_future()` instead, since that can work
    # with futures. But I don't like ensure_future.)
    #
    # (Another side note: I don't think we even need `create_task()` or
    # `ensure_future()`...If you don't want a result, you can just call
    # `shutdown_waits_for()` as a flat function call, no await or anything,
    # and it should still work.

    async def inner():
        return await fut

    return inner()


def _shutdown(loop=None):
    logger.debug('Entering shutdown handler')
    loop = loop or get_event_loop()
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)
    logger.critical('Stopping the loop')
    loop.call_soon_threadsafe(loop.stop)


def run(coro: Optional[Coroutine] = None, *,
        loop: Optional[AbstractEventLoop] = None,
        shutdown_handler: Optional[Callable[[], None]] = None,
        executor_workers: int = 10,
        executor: Optional[Executor] = None) -> None:
    logger.debug('Entering run()')
    loop = loop or get_event_loop()
    if coro:
        async def new_coro():
            """During shutdown, run_until_complete() will exit
            if a CancelledError bubbles up from anything in the
            group. To counteract that, we'll try to handle
            any CancelledErrors that bubble up from the given
            coro. This isn't fool-proof: if the user doesn't
            provide a coro, and instead creates their own with
            loop.create_task, that task might bubble
            a CancelledError into the run_until_complete()."""
            try:
                await coro
            except asyncio.CancelledError:
                pass
        loop.create_task(new_coro())
    shutdown_handler = shutdown_handler or partial(_shutdown, loop)
    loop.add_signal_handler(SIGINT, shutdown_handler)
    loop.add_signal_handler(SIGTERM, shutdown_handler)
    if not executor:
        logger.debug('Creating default executor')
        executor = ThreadPoolExecutor(max_workers=executor_workers)
    loop.set_default_executor(executor)
    logger.critical('Running forever.')
    loop.run_forever()
    logger.critical('Entering shutdown phase.')

    def sep():
        tasks = Task.all_tasks(loop=loop)
        do_not_cancel = set()
        for t in tasks:
            if t._coro in _DO_NOT_CANCEL_COROS:
                do_not_cancel.add(t)

        tasks -= do_not_cancel

        logger.critical('Cancelling pending tasks.')
        for t in tasks:
            print('Cancelling task: ', t)
            t.cancel()
        return tasks, do_not_cancel

    tasks, do_not_cancel = sep()
    # Here's a protip: if you group a bunch of tasks, and some of them
    # get cancelled, and they DON'T HANDLE THE CANCELLATION, then the
    # raised CancelledError will bubble up to, and stop the
    # loop.run_until_complete() line.
    group = gather(*tasks, *do_not_cancel, return_exceptions=True)
    logger.critical('Running pending tasks till complete')
    loop.run_until_complete(group)

    logger.critical('Waiting for executor shutdown.')
    executor.shutdown(wait=True)
    logger.critical('Closing the loop.')
    loop.close()
    logger.critical('Leaving. Bye!')
