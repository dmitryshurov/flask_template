from apps.backend.app import app

with app.app_context():
    from components import todo_list, users

    app.register_blueprint(todo_list.blueprint)
    app.register_blueprint(users.blueprint)


@app.cli.command('db_create')
def db_create():
    app.logger.info('Creating DB...')
    app.db.create_all()
    app.logger.info('DB created')


@app.cli.command('db_drop')
def db_drop():
    app.logger.info('Dropping DB...')
    app.db.drop_all()
    app.logger.info('DB dropped')
