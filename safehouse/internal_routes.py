from panic.views import random, inform
from collections import defaultdict
from functools import partial

"""This file contains all of the views that request types can call.
   AKA an sms request can call panic, etc."""


# If app requested doesn't exist, fail silently
def black_hole(*args, **kwargs):
    return None


SMS_ROUTES = defaultdict(lambda: black_hole)
SMS_ROUTES.update({"panic": random,
                   "inform": inform,
                   })
