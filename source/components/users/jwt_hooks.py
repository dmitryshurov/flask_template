from flask import current_app as app

from .models import TokenBlocklist, User


@app.jwt.token_in_blocklist_loader
def check_if_token_revoked(_, jwt_payload):
    jti = jwt_payload["jti"]
    token = app.db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@app.jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    current_user_email = jwt_data["sub"]
    return User.query.filter_by(email=current_user_email).one_or_none()
