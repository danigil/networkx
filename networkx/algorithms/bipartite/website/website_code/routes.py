from . import app


@app.route('/home')
def home_page():
    return 'HELLO'
