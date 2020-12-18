from flask import Flask, Blueprint
from main import main as main_blueprint
from auth import auth as auth_blueprint
from flask_login import LoginManager
from initdb import Users, sess



app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return sess.query(Users).get(int(user_id))

app.register_blueprint(main_blueprint, url_prefix='/')
app.register_blueprint(auth_blueprint, url_prefix='/')

app.secret_key = "6d97f134fc912601484a9336"


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", use_reloader=False)
