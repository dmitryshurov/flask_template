from .app import app

with app.app_context():
    from components import todo_list, users

    app.register_blueprint(todo_list.blueprint)
    app.register_blueprint(users.blueprint)

app.db.drop_all()
app.db.create_all()


@app.cli.command('db_init')
def db_init():
    app.db.create_all()
