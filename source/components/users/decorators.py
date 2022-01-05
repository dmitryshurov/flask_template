from functools import wraps

from flask import current_app as app, request
from flask_jwt_extended import current_user, verify_jwt_in_request


def auth_required(roles_required=None, optional=False, fresh=False, refresh=False, locations=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            def access_denied():
                return {'msg': 'Access denied'}, 401

            app.logger.info(f'Cookies: {request.cookies}')

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
