from datetime import datetime, timezone

from flask import current_app as app
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies
from marshmallow import ValidationError

from .models import TokenBlocklist, User


@app.jwt.token_in_blocklist_loader
def check_if_token_revoked(_, jwt_payload):
    jti = jwt_payload['jti']
    token = app.db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@app.jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    current_user_email = jwt_data['sub']
    return User.query.filter_by(email=current_user_email).one_or_none()


@app.errorhandler(ValidationError)
def handle_bad_request(e):
    return {'err': {'validation': e.messages}}, 400


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + app.config['JWT_REFRESH_TOKEN_BEFORE'])
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # If there is no valid JWT, just return the original respone
        return response
