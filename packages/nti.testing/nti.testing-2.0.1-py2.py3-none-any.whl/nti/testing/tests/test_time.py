#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function,  absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#disable: accessing protected members, too many methods
#pylint: disable=W0212,R0904

import unittest
from hamcrest import assert_that
from hamcrest import is_
from hamcrest import greater_than
from hamcrest import greater_than_or_equal_to
from hamcrest import less_than

from nti.testing.time import time_monotonically_increases, reset_monotonic_time

class TestTime(unittest.TestCase):

    def _check_time(self, granularity=1.0):
        import time
        for _ in range(10):
            before = time.time()
            after = time.time()
            assert_that(after, is_(greater_than_or_equal_to(before + granularity)))
        return after

    @time_monotonically_increases
    def test_increases_in_method(self):
        self._check_time()

    def test_increases_in_func(self):

        @time_monotonically_increases
        def f():
            self._check_time()

        f()

    def test_func_takes_args(self):

        @time_monotonically_increases
        def f(a, b, c=42):
            return a, b, c

        assert_that(f(1, 2), is_((1, 2, 42)))
        assert_that(f(1, 2, 3), is_((1, 2, 3)))
        assert_that(f(1, 2, c=9), is_((1, 2, 9)))

    def test_increases_relative_to_real(self):
        import time
        before_all = time.time()

        @time_monotonically_increases
        def f():
            return self._check_time()

        after_first = f()
        assert_that(after_first, is_(greater_than(before_all)))


    def test_increases_across_funcs(self):
        reset_monotonic_time()

        granularity = 0.1
        import time
        before_all = time.time()

        @time_monotonically_increases(granularity)
        def f1():
            return self._check_time(granularity)

        @time_monotonically_increases(granularity)
        def f2():
            return self._check_time(granularity)

        after_first = f1()

        assert_that(after_first, is_(greater_than(before_all)))

        after_second = f2()
        current_real = time.time()

        # The loop in self._check_time incremented the clock by a full second.
        # That function should have taken far less time to actually run than that, though,
        # so the real time function should be *behind*
        assert_that(current_real, is_(less_than(after_second)))


        # And immediately running it again will continue to produce values that
        # are ever larger.
        after_second = f2()
        current_real = time.time()

        assert_that(current_real, is_(less_than(after_second)))

        assert_that(after_second, is_(greater_than(before_all)))
        assert_that(after_second, is_(greater_than(after_first)))

        # We are now some number of seconds ahead. If we're the only ones calling
        # time.time(), it would be about 3. But we're not, various parts of the lib
        # apparently are calling time.time() too, which makes it unpredictable.
        # We don't want to sleep for a long time, so we
        # reset the clock again to prove that we can go back to real time.
        @time_monotonically_increases(granularity)
        def f3():
            return time.time()

        # Use a value in the distant past to account for the calls that get made.
        reset_monotonic_time(-50)

        after_third = f3()
        current_real = time.time()
        assert_that(current_real, is_(greater_than_or_equal_to(after_third)))

if __name__ == '__main__':
    unittest.main()
