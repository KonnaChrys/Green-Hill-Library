from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# πινακας βιβλιων

class Book(db.Model):

    __tablename__ = "books"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    isbn = db.Column(
        db.String(20),
        unique=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    authors = db.Column(
        db.String(255)
    )

    publisher = db.Column(
        db.String(255)
    )

    year = db.Column(
        db.Integer
    )

    pages = db.Column(
        db.Integer
    )

    language = db.Column(
        db.String(50)
    )

    cover_type = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    categories = db.Column(
        db.Text
    )

    cover_url = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(50),
        default="Available"
    )

    copies = db.Column(
        db.Integer,
        default=1
    )
    
    total_copies = db.Column(
        db.Integer,
        default=1
    )

    loans = db.relationship(
        "Loan",
        backref="book",
        lazy=True
    )

    def __repr__(self):

        return f"<Book {self.title}>"


# πινακας μελων

class Member(db.Model):

    __tablename__ = "members"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    card_number = db.Column(
        db.String(13),
        unique=True,
        nullable=False
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(50)
    )

    date_of_birth = db.Column(
        db.Date
    )

    address = db.Column(
        db.String(255)
    )

    balance = db.Column(
        db.Float,
        default=0
    )

    loans = db.relationship(
        "Loan",
        backref="member",
        lazy=True
    )

    def __repr__(self):

        return (
            f"<Member "
            f"{self.first_name} "
            f"{self.last_name}>"
        )
    

# πινακας ιστορικου δανεισμων

class Loan(db.Model):

    __tablename__ = "loans"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("books.id"),
        nullable=False
    )

    borrow_date = db.Column(
        db.Date,
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    return_date = db.Column(
        db.Date
    )

    status = db.Column(
        db.String(50),
        default="Borrowed"
    )

    fine = db.Column(
        db.Float,
        default=0
    )

    paid = db.Column(
        db.Boolean,
        default=False
    )