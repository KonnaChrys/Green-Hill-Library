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


@app.route("/book/<int:id>")
def book_info(id):

    book = Book.query.get_or_404(id)

    return render_template(
        "book_info.html",
        book=book
    )


@app.route("/edit-book/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    book = Book.query.get_or_404(id)

    if request.method == "POST":

        book.isbn = request.form["isbn"]

        book.title = request.form["title"]

        book.authors = request.form["authors"]

        book.publisher = request.form["publisher"]

        book.year = request.form["year"] or None

        book.pages = request.form["pages"] or None

        book.language = request.form["language"]

        book.cover_url = request.form["cover_url"]

        book.copies = request.form["copies"] or 1

        db.session.commit()

        return redirect(f"/book/{book.id}")

    return render_template(
        "edit_book.html",
        book=book
    )


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)