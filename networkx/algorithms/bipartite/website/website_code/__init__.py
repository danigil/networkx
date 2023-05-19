from flask import Flask

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="123",
    WTF_CSRF_SECRET_KEY="123"
))
from . import routes