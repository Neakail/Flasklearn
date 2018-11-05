from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
# from flask_script import Manager
# from flask_bootstrap import Bootstrap
from flask import render_template

app = Flask(__name__)
# manager = Manager(app)


# @app.route('/')
# def index():
#     return '<h1>Hello World!</h1>'

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is % s</p>' % user_agent

# @app.route('/cookie')
# def index():
#     response = make_response('<h1>This document carries a cookie!</h1>')
#     response.set_cookie('answer', '42')
#     return response

# @app.route('/redirect')
# def index():
#     return redirect('http://www.example.com')

# @app.route('/user/<name>')
# def user(name):
#     return '<h1>Hello, % s!</h1>' % name

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/user/<id>')
def get_user(id):
    user = abort.load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, % s</h1>' % user.name

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# url_for('user', name='john', _external=True)
#

if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
