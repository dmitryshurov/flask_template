import os
import uuid
from functools import wraps

import bcrypt
from flask import Blueprint, current_app as app, request
from flask_jwt_extended import (
    create_access_token,
    current_user,
    get_jwt,
    jwt_required,
    verify_jwt_in_request
)
from marshmallow import fields
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from components.users import auth_required

blueprint = Blueprint('todo_list', __name__, url_prefix='/todo_list')


class TodoList(app.db.Model):
    __tablename__ = 'todo_list'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))


class TodoListItem(app.db.Model):
    __tablename__ = 'todo_list_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    todo_list_id = Column(Integer, ForeignKey('todo_list.id'))
    is_done = Column(Boolean, server_default='FALSE')


class TodoListSchema(app.ma.Schema):
    class Meta:
        additional = ('id', 'title', 'user_id')
        ordered = True


todo_list_schema = TodoListSchema()
todo_lists_schema = TodoListSchema(many=True)


@blueprint.route('/todo_lists', methods=['GET'])
# @auth_required(['admin'])
def get_todo_lists():
    return {'todo_lists': todo_lists_schema.dump(TodoList.query.all())}


@blueprint.route('/todo_lists', methods=['POST'])
# @auth_required(['admin'])
def create_todo_list():

    todo_list = TodoList(title='Test', user_id=1)
    app.db.session.add(todo_list)
    app.db.session.commit()
    return {'msg': 'TODO List created'}
