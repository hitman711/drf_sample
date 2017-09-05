""" List of throttling functions
  BurstRateThrottle
  SustainedRateThrottle
"""
import time
from rest_framework import throttling

from rest_framework.compat import is_authenticated
from django.conf import settings

from django.core.cache import cache as default_cache
from django.core.exceptions import ImproperlyConfigured


class CustomThrottle(throttling.BaseThrottle):
    """
    A simple cache implementation, that only requires `.get_cache_key()`
    to be overridden.

    The rate (requests / seconds) is set by a `throttle` attribute on the View
    class.
    The attribute is a string of the form 'number_of_requests/period'.
    Period should be one of: ('s', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day')
    """
    cache = default_cache
    timer = time.time
    cache_format = 'throttle_%(scope)s_%(ident)s'
    scope = 'burst'
    save_duration = 10
    extended_limit = ''
    THROTTLE_RATES = settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']

    def __init__(self):
        if not getattr(self, 'rate', None):
            self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)
        print (self.num_requests, self.duration)

    def get_rate(self):
        """
        Determine the string representation of the allowed request rate.
        """
        if not getattr(self, 'scope', None):
            msg = ("You must set either `.scope` or `.rate` for '%s' throttle" %
                   self.__class__.__name__)
            raise ImproperlyConfigured(msg)

    def get_rate(self):
        """
        Determine the string representation of the allowed request rate.
        """
        if not getattr(self, 'scope', None):
            msg = ("You must set either `.scope` or `.rate` for '%s' throttle" %
                   self.__class__.__name__)
            raise ImproperlyConfigured(msg)

        try:
            return self.THROTTLE_RATES[self.scope]
        except KeyError:
            msg = "No default throttle rate set for '%s' scope" % self.scope
            raise ImproperlyConfigured(msg)

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        return (num_requests, duration)

    def get_cache_key(self, request, view):
        """
        """
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            if self.save_duration > self.now - self.history[0]:
                return False

        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
        return True

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        if self.history:
            remaining_duration =  self.now - self.history[-1]
        else:
            remaining_duration = self.save_duration

        available_requests = self.num_requests - len(self.history) + 1
        if available_requests <= 0:
            return None
        return remaining_duration / available_requests
