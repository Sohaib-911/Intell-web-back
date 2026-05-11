"""
Rate limiting utilities using SlowAPI.
Configured for the contact form endpoint.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
