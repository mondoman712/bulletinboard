from flask import Flask, render_template, request
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'Ludlk5uG5GWWrkPnwfwZuWeVcYuBlwaVc9AS8oUo'


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    form1 = EnterDBInfo(request.form)

    if request.method == 'POST' and form1.validate():
        data_entered = Data(notes=form1.dbNotes.data)
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html', notes=form1.dbNotes.data,
               data=data_entered)

    try:
        query_dbb = Data.query.order_by(Data.id.desc()).limit(10)
        for q in query_dbb:
            print(q.notes)
        db.session.close()
    except:
        db.session.rollback()

    return render_template('index.html', form1=form1, results=query_dbb)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
