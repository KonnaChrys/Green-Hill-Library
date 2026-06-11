import os

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

        cover_file = request.files.get("cover_upload")

        cover_url = request.form["cover_url"]

        if cover_file and cover_file.filename != "":

            filepath = os.path.join(
                "static",
                "uploads",
                cover_file.filename
            )

            cover_file.save(filepath)

            cover_url = "/" + filepath.replace("\\", "/")

        book = Book(

            isbn=request.form["isbn"],

            title=request.form["title"],

            authors=request.form["authors"],

            publisher=request.form["publisher"],

            year=request.form["year"] or None,

            pages=request.form["pages"] or None,

            language=request.form["language"],

            cover_type=request.form["cover_type"],

            description=request.form["description"],

            categories=",".join(request.form.getlist("categories")),

            cover_url=cover_url,

            copies=request.form["copies"] or 1

        )

        db.session.add(book)

        db.session.commit()

        return redirect("/books")

    return render_template("add_book.html")


@app.route("/books")
def books():

    search = request.args.get("search", "")

    categories = request.args.getlist("categories")

    language = request.args.get("language", "")

    year = request.args.get("year", "")

    pages = request.args.get("pages", "")

    available_only = request.args.get("available_only")

    # ΑΥΤΟ ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ ΕΔΩ
    query = Book.query

    if search:

        query = query.filter(
            (Book.title.ilike(f"%{search}%")) |
            (Book.authors.ilike(f"%{search}%"))
        )

    if categories:

        for category in categories:

            query = query.filter(
                Book.categories.ilike(f"%{category}%")
            )

    if language and language != "Όλες":

        query = query.filter(
            Book.language == language
        )

    if year == "Πριν το 1950":

        query = query.filter(Book.year < 1950)

    elif year == "1950-1979":

        query = query.filter(
            Book.year >= 1950,
            Book.year <= 1979
        )

    elif year == "1980-1999":

        query = query.filter(
            Book.year >= 1980,
            Book.year <= 1999
        )

    elif year == "2000-2009":

        query = query.filter(
            Book.year >= 2000,
            Book.year <= 2009
        )

    elif year == "2010-2019":

        query = query.filter(
            Book.year >= 2010,
            Book.year <= 2019
        )

    elif year == "2020+":

        query = query.filter(
            Book.year >= 2020
        )

    # Σελίδες

    if pages == "1-100":

        query = query.filter(
            Book.pages >= 1,
            Book.pages <= 100
        )

    elif pages == "101-200":

        query = query.filter(
            Book.pages >= 101,
            Book.pages <= 200
        )

    elif pages == "201-300":

        query = query.filter(
            Book.pages >= 201,
            Book.pages <= 300
        )

    elif pages == "301-400":

        query = query.filter(
            Book.pages >= 301,
            Book.pages <= 400
        )

    elif pages == "401-500":

        query = query.filter(
            Book.pages >= 401,
            Book.pages <= 500
        )

    elif pages == "500+":

        query = query.filter(
            Book.pages >= 500
        )

    # Διαθεσιμότητα

    if available_only:

        query = query.filter(
            Book.status == "Available"
        )

    books = query.all()

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

    # Ελεγχος αν το νεο ISBN υπαρχει ηδη σε αλλο βιβλιο

    if request.method == "POST":

        new_isbn = request.form["isbn"]

        cover_file = request.files.get("cover_upload")

        cover_url = request.form["cover_url"]

        if cover_file and cover_file.filename != "":

            filepath = os.path.join(
                "static",
                "uploads",
                cover_file.filename
            )

            cover_file.save(filepath)

            cover_url = "/" + filepath.replace("\\", "/")

        existing = Book.query.filter_by(
            isbn=new_isbn
        ).first()

        if existing and existing.id != book.id:

            return "Υπάρχει ήδη βιβλίο με αυτό το ISBN"

        book.isbn = new_isbn

        book.title = request.form["title"]

        book.authors = request.form["authors"]

        book.publisher = request.form["publisher"]

        book.year = request.form["year"] or None

        book.pages = request.form["pages"] or None

        book.language = request.form["language"]

        book.cover_type = request.form["cover_type"]

        book.description = request.form["description"]

        book.categories = ",".join(request.form.getlist("categories"))

        book.cover_url = cover_url

        book.copies = request.form["copies"] or 1

        db.session.commit()

        return redirect(f"/book/{book.id}")

    return render_template(
        "edit_book.html",
        book=book
    )

@app.route("/delete-book/<int:id>", methods=["POST"])
def delete_book(id):

    book = Book.query.get_or_404(id)

    db.session.delete(book)

    db.session.commit()

    return redirect("/books")

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)