from init import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    pwhash = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f'<User {self.id}, {self.nome}, {self.email}, {self.pwhash}>'
