from flask import Flask, render_template, request
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo, LoginForm
from login import LoginManager
# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'Ludlk5uG5GWWrkPnwfwZuWeVcYuBlwaVc9AS8oUo'

login_manager = LoginManager()
login_manager.init_app(app)

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)
"""
@application.route('/login')
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(user)
        flash('Logged in')
        next = request.args.get('next')

        if not next_is_valid(next):
            return abort(400)

        return redirect(next or flask.url_for('index'))
        return render_template('login.html', form1=form)
"""
@application.route('/user/<uname>')
def show_user(uname):
    try:
        query_db = Data.query.filter(Data.username==uname)
        db.session.close()
    except:
        print('ERROR')
        db.session.rollback()
    return render_template('user.html', results=query_db)

@application.route('/post/<int:post_id>')
def show_post(post_id):
    try:
        query_db = Data.query.filter(Data.id==post_id)
        db.session.close()
    except:
        print('ERROR')
        db.session.rollback()
    return render_template('post.html', results=get_first(query_db))

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    form1 = EnterDBInfo(request.form)

    if request.method == 'POST' and form1.validate():
        data_entered = Data(notes=form1.dbNotes.data,
                username=form1.dbUsername.data)
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

    try:
        query_dbb = Data.query.order_by(Data.id.desc()).limit(10)
        db.session.close()
    except:
        db.session.rollback()

    return render_template('index.html', form1=form1, results=query_dbb)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
