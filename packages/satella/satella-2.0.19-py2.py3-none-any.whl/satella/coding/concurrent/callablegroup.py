# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import logging
from ..typecheck import typed, Callable

logger = logging.getLogger(__name__)


__all__ = [
    'CallableGroup',
]

class CallableGroup(object):
    """
    This behaves like a function, but allows to add other functions to call
    when invoked, eg.

        c1 = Callable()

        c1.add(foo)
        c1.add(bar)

        c1(2, 3)

    Now both foo and bar will be called with arguments (2, 3). Their exceptions
    will be propagated.

    """

    # todo not threadsafe with oneshots

    def __init__(self, gather=False, swallow_exceptions=False):
        """
        :param gather: if True, results from all callables will be gathered
                       into a list and returned from __call__
        :param swallow_exceptions: if True, exceptions from callables will be
                                   silently ignored. If gather is set,
                                   result will be the exception instance
        """
        self.callables = []  # tuple of (callable, oneshot)
        self.gather = gather
        self.swallow_exceptions = swallow_exceptions

    @typed(None, Callable, bool)
    def add(self, callable, oneshot=False):
        """
        :param oneshot: if True, callable will be unregistered after single call
        """
        self.callables.append((callable, oneshot))

    def __call__(self, *args, **kwargs):
        """
        Run the callable. All registered callables will be called with
        passed arguments, so they should have the same arity.

        If callables raise, it will be passed through.

        :return: list of results if gather was set, else None
        """
        clbl = self.callables  # for moar thread safety
        self.callables = []

        if self.gather:
            results = []

        for callable, oneshot in clbl:
            try:
                q = callable(*args, **kwargs)
            except Exception as e:
                if not self.swallow_exceptions:
                    raise  # re-raise
                q = e

            if self.gather:
                results.append(q)

            if not oneshot:
                self.callables.append((callable, oneshot))

        if self.gather:
            return results


