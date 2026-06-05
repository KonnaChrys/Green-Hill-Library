from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)

    isbn = db.Column(db.String(20), unique=True)

    title = db.Column(db.String(255), nullable=False)

    publisher = db.Column(db.String(255))

    year = db.Column(db.Integer)

    pages = db.Column(db.Integer)

    language = db.Column(db.String(50))

    cover_url = db.Column(db.Text)

    status = db.Column(
        db.String(50),
        default="Available"
    )

    copies = db.Column(
        db.Integer,
        default=1
    )

    def __repr__(self):
        return f"<Book {self.title}>"