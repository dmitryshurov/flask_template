from functools import wraps

from flask_jwt_extended import current_user, verify_jwt_in_request


def auth_required(roles_required=None, optional=False, fresh=False, refresh=False, locations=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            def access_denied():
                return {'message': "Access denied"}, 401

            verify_jwt_in_request(optional, fresh, refresh, locations)

            if not current_user:
                return access_denied()

            if not current_user.is_active:
                return access_denied()

            if roles_required is None:
                return fn(*args, **kwargs)

            if current_user.role not in roles_required:
                return access_denied()

            return fn(*args, **kwargs)

        return decorator

    return wrapper
