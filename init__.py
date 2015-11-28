from flask import Flask
application = Flask(__name__)
application.debug=True

@application.route('/', methods=['GET', 'POST'])

def home():
    return "heyyo"

if __name__ == '__main__':
    application.run(host='0.0.0.0')
