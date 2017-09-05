""" List of throttling functions
  BurstRateThrottle
  SustainedRateThrottle
"""
from rest_framework import throttling

class BurstRateThrottle(throttling.AnonRateThrottle):
    """ Throttle value after user reach daily limit
    """
    scope = 'burst'

class SustainedRateThrottle(throttling.AnonRateThrottle):
    """ Throttle API hit limit defined
    """
    scope = 'sustained'
