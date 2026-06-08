from flask import Flask, render_template, request, redirect

from models import db, Book

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "mysql+pymysql://root:@localhost/library"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/add-book", methods=["GET", "POST"])
def add_book():

    if request.method == "POST":

        book = Book(

            isbn=request.form["isbn"],

            title=request.form["title"],

            authors=request.form["authors"],

            publisher=request.form["publisher"],

            year=request.form["year"] or None,

            pages=request.form["pages"] or None,

            language=request.form["language"],

            cover_url=request.form["cover_url"],

            copies=request.form["copies"] or 1

        )

        db.session.add(book)

        db.session.commit()

        return redirect("/books")

    return render_template("add_book.html")

@app.route("/books")
def books():

    books = Book.query.all()

    return render_template(
        "view_books.html",
        books=books
    )

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)