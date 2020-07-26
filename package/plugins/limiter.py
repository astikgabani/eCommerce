"""
Format of the rate-limit string
[count] [per|/] [n (optional)] [second|minute|hour|day|month|year]
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["5000/day", "750/hour"])
