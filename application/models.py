from application import db

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(128), index=True, unique=False)
    username = db.Column(db.String(128), index=True, unique=False)
    
    def __init__(self, notes, username):
        self.notes = notes
        self.username = username

    def __repr__(self):
        return '<Data %r, %r>' % (self.notes, self.username)