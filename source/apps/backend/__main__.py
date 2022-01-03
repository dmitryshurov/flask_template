from .app import app, db
from components import users

app.register_blueprint(users.blueprint)

db.drop_all()
db.create_all()

if __name__ == '__main__':
    app.run()
