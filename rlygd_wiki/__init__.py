from flask import Flask
from flask_bootstrap import Bootstrap
from rlygd_wiki import routes

app = Flask(__name__)
app.register_blueprint(routes.mod)

app.config.from_object(__name__)
Bootstrap(app)
