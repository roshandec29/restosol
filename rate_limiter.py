
from fastapi import HTTPException, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

RATE_LIMIT_ENABLED = True
RATE_LIMIT_DEFAULT = "5/second"


# Custom Exception
class RateLimitException(HTTPException):
    def __init__(self):
        super().__init__(status_code=429, detail={"status": 0, "message": "Too many requests"})


async def get_limiter():
    return Limiter(key_func=get_remote_address)


# Custom Rate Limit Decorator
def custom_ratelimit(rate: str = None, key_func=None):
    def decorator(view_func):
        async def wrapper(request: Request, limiter_instance: Limiter = Depends(get_limiter), *args, **kwargs):
            if not RATE_LIMIT_ENABLED:
                return await view_func(request, *args, **kwargs)

            effective_rate = rate or RATE_LIMIT_DEFAULT

            if key_func:
                key = key_func(request)
                if key is None:
                    return await view_func(request, *args, **kwargs)

                limiter_instance_custom = Limiter(key_func=key_func)
                if limiter_instance_custom.limit(effective_rate, key):
                    return await view_func(request, *args, **kwargs)
                else:
                    raise RateLimitException()
            else:
                if limiter_instance.limit(effective_rate, request.client.host):
                    return await view_func(request, *args, **kwargs)
                else:
                    raise RateLimitException()
        return wrapper
    return decorator
