import os

from flask import Flask, render_template, request, redirect, jsonify, url_for
from models import db, Book, Member, Loan
from datetime import datetime, timedelta

app = Flask(__name__)

# συνδεση με τη βαση δεδομενων

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "mysql+pymysql://root:@localhost/library"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# αρχικη σελιδα

@app.route("/")
def home():

    return render_template("index.html")


#------------------- βιβλια -------------------

# προσθηκη βιβλιου

@app.route("/add-book", methods=["GET", "POST"])
def add_book():

    if request.method == "POST":

        # ελεγχος αν ανεβηκε εικονα

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

        # δημιουργια νεου βιβλιου

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

            categories=",".join(
                request.form.getlist("categories")
            ),

            cover_url=cover_url,

            copies=request.form["copies"] or 1

        )

        db.session.add(book)

        db.session.commit()

        return redirect("/books")

    return render_template("add_book.html")


# λιστα βιβλιων και φιλτρα

@app.route("/books")
def books():

    search = request.args.get("search", "")

    categories = request.args.getlist("categories")

    language = request.args.get("language", "")

    year = request.args.get("year", "")

    pages = request.args.get("pages", "")

    available_only = request.args.get(
        "available_only"
    )

    # αρχικο query

    query = Book.query

    # αναζητηση

    if search:

        query = query.filter(
            (Book.title.ilike(f"%{search}%")) |
            (Book.authors.ilike(f"%{search}%"))
        )

    # κατηγοριες

    if categories:

        for category in categories:

            query = query.filter(
                Book.categories.ilike(
                    f"%{category}%"
                )
            )

    # γλωσσα

    if language and language != "Όλες":

        query = query.filter(
            Book.language == language
        )

    # ετος

    if year == "Πριν το 1950":

        query = query.filter(
            Book.year < 1950
        )

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

    # σελιδες

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

    # διαθεσιμοτητα

    if available_only:

        query = query.filter(
            Book.status == "Available"
        )

    books = query.all()

    return render_template(
        "view_books.html",
        books=books
    )


# στοιχεια βιβλιου

@app.route("/book/<int:id>")
def book_info(id):

    book = Book.query.get_or_404(id)

    return render_template(
        "book_info.html",
        book=book
    )


# επεξεργασια βιβλιου

@app.route(
    "/edit-book/<int:id>",
    methods=["GET", "POST"]
)
def edit_book(id):

    book = Book.query.get_or_404(id)

    if request.method == "POST":

        new_isbn = request.form["isbn"]

        cover_file = request.files.get(
            "cover_upload"
        )

        cover_url = request.form["cover_url"]

        # ελεγχος για νεα εικονα

        if cover_file and cover_file.filename != "":

            filepath = os.path.join(
                "static",
                "uploads",
                cover_file.filename
            )

            cover_file.save(filepath)

            cover_url = "/" + filepath.replace(
                "\\",
                "/"
            )

        # ελεγχος για διπλο isbn

        existing = Book.query.filter_by(
            isbn=new_isbn
        ).first()

        if existing and existing.id != book.id:

            return "Υπάρχει ήδη βιβλίο με αυτό το ISBN"

        # ενημερωση στοιχειων

        book.isbn = new_isbn

        book.title = request.form["title"]

        book.authors = request.form["authors"]

        book.publisher = request.form["publisher"]

        book.year = request.form["year"] or None

        book.pages = request.form["pages"] or None

        book.language = request.form["language"]

        book.cover_type = request.form["cover_type"]

        book.description = request.form[
            "description"
        ]

        book.categories = ",".join(
            request.form.getlist("categories")
        )

        book.cover_url = cover_url

        book.copies = request.form["copies"] or 1

        db.session.commit()

        return redirect(
            f"/book/{book.id}"
        )

    return render_template(
        "edit_book.html",
        book=book
    )


# διαγραφη βιβλιου

@app.route(
    "/delete-book/<int:id>",
    methods=["POST"]
)
def delete_book(id):

    book = Book.query.get_or_404(id)

    db.session.delete(book)

    db.session.commit()

    return redirect("/books")


#------------------- μελη -------------------

# λιστα μελων

@app.route("/members")
def members():

    members = Member.query.all()

    return render_template(
        "view_members.html",
        members=members
    )

# πληροφοριες μελους

@app.route(
    "/member/<int:id>"
)
def member_info(id):

    member = Member.query.get_or_404(
        id
    )

    loans = Loan.query.filter_by(

        member_id=member.id

    ).all()

    return render_template(

        "member_info.html",

        member=member,

        loans=loans

    )


# προσθηκη μελους

@app.route(
    "/add-member",
    methods=["GET", "POST"]
)
def add_member():

    # βρισκει το τελευταιο μελος

    last_member = Member.query.order_by(
        Member.id.desc()
    ).first()

    # δημιουργει επομενο αριθμο καρτας

    if last_member:

        next_card_number = str(
            int(last_member.card_number) + 1
        ).zfill(13)

    else:

        next_card_number = "0000000000001"

    if request.method == "POST":

        member = Member(

            card_number=next_card_number,

            first_name=request.form["first_name"],

            last_name=request.form["last_name"],

            phone=request.form["phone"],

            date_of_birth=datetime.strptime(
                request.form["date_of_birth"],
                "%Y-%m-%d"
            ).date(),

            address=request.form["address"]

        )

        db.session.add(member)

        db.session.commit()

        return redirect("/members")

    return render_template(

        "add_member.html",

        next_card_number=next_card_number

    )

# δανεισμος βιβλιου

#------------------- δανεισμοι -------------------

@app.route("/loans")
def loans():

    member_id = request.args.get(
        "member_id"
    )

    book_id = request.args.get(
        "book_id"
    )

    member = None
    book = None

    if member_id:

        member = Member.query.get_or_404(
            member_id
        )

    if book_id:

        book = Book.query.get_or_404(
            book_id
        )

    return render_template(

        "loans.html",

        member=member,

        book=book

    )

# api μελους

@app.route(
    "/api/member/<card_number>"
)
def api_member(card_number):

    member = Member.query.filter_by(
        card_number=card_number
    ).first()

    if not member:

        return jsonify(
            {
                "found": False
            }
        )

    return jsonify(

        {
            "found": True,

            "first_name":
                member.first_name,

            "last_name":
                member.last_name,

            "phone":
                member.phone,

            "balance":
                member.balance

        }

    )

# api βιβλιου

@app.route(
    "/api/book/<isbn>"
)
def api_book(isbn):

    book = Book.query.filter_by(
        isbn=isbn
    ).first()

    if not book:

        return jsonify(
            {
                "found": False
            }
        )

    return jsonify(

        {
            "found": True,

            "title":
                book.title,

            "authors":
                book.authors,

            "publisher":
                book.publisher,

            "year":
                book.year,

            "language":
                book.language

        }

    )

@app.route(
    "/save-loan",
    methods=["POST"]
)
def save_loan():

    data = request.get_json()

    member = Member.query.filter_by(

        card_number=data["member_card"]

    ).first()

    if not member:

        return jsonify(

            {

                "success": False,

                "message": "Δεν βρέθηκε μέλος"

            }

        )

    active_loans = Loan.query.filter_by(

        member_id=member.id,

        status="Borrowed"

    ).count()

    if (

        active_loans +

        len(data["books"])

    ) > 10:

        return jsonify(

            {

                "success": False,

                "message":

                "Το μέλος δεν μπορεί να έχει πάνω από 10 δανεισμένα βιβλία"

            }

        )

    for isbn in data["books"]:

        book = Book.query.filter_by(

            isbn=isbn

        ).first()

        if not book:

            continue

        if book.status == "Borrowed":

            continue

        book.status = "Borrowed"

        loan = Loan(

            member_id=member.id,

            book_id=book.id,

            borrow_date=datetime.today().date(),

            due_date=(

                datetime.today() +

                timedelta(days=30)

            ).date(),

            status="Borrowed"

        )

        db.session.add(

            loan

        )

    db.session.commit()

    return jsonify(

        {

            "success": True

        }

    )

@app.route(
    "/returns"
)
def returns():

    loans = Loan.query.filter_by(

        status="Borrowed"

    ).all()

    return render_template(

        "returns.html",

        loans=loans

    )

@app.route(
    "/return-book/<int:loan_id>"
)
def return_book(loan_id):

    loan = Loan.query.get_or_404(
        loan_id
    )

    book = Book.query.get(
        loan.book_id
    )

    member = Member.query.get(
        loan.member_id
    )

    today = datetime.today().date()

    loan.status = "Returned"

    loan.return_date = today

    book.status = "Available"

    if(

        today >

        loan.due_date

    ):

        days = (

            today -

            loan.due_date

        ).days

        loan.fine = (

            days * 0.50

        )

        member.balance += (

            days * 0.50

        )

    db.session.commit()

    return redirect(

        url_for(

            "returns"

        )

    )

@app.route(
    "/pay-loan/<int:loan_id>"
)
def pay_loan(loan_id):

    loan = Loan.query.get_or_404(
        loan_id
    )

    if not loan.paid:

        member = Member.query.get(
            loan.member_id
        )

        member.balance -= loan.fine

        loan.paid = True

        db.session.commit()

    return redirect(

        url_for(

            "member_info",

            id=loan.member_id

        )

    )

# εκκινηση εφαρμογης

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)