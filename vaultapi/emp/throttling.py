from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class AnoThrottle(AnonRateThrottle):
    scope = 'ano'

class UserThrottleRate(UserRateThrottle):
    scope = 'user'





