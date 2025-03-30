from functools import wraps

from starlette.responses import Response


def has_permissions(*permission_classes, method=any):
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")

            if method(
                [perm_class().has_perm(request) for perm_class in permission_classes]
            ):
                return await f(*args, **kwargs)

            return Response(status_code=403)
        return wrapper
    return decorator
