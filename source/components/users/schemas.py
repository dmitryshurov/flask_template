from flask import current_app as app
from marshmallow import fields


class UserSchema(app.ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(dump_only=True)
    is_active = fields.Boolean(dump_only=True)

    class Meta:
        additional = ('id', 'uuid')
        ordered = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)
