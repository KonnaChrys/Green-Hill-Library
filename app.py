import os

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from models import db, Book, Member, Loan
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.getenv(
    "SECRET_KEY",
    "library_system_secret_key"
)


# συνδεση με τη βαση δεδομενων

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(

    "DATABASE_URL",

    "mysql+pymysql://root:@localhost/library"

)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
print(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)


# ενημερωση συνολικου υπολοιπου μελους

def update_member_balance(member_id):

    member = Member.query.get(

        member_id

    )

    balance = 0

    for loan in member.loans:

        if not loan.paid:

            balance += loan.fine

    member.balance = balance

    db.session.commit()


#------------------- αρχικη -------------------


# αρχικη σελιδα

@app.route("/")
def home():

    return render_template(

        "index.html"

    )


#------------------- βιβλια -------------------


# προσθηκη βιβλιου

@app.route(
    "/add-book",
    methods=["GET", "POST"]
)
def add_book():

    if request.method == "POST":

        # ελεγχος αν ανεβηκε εικονα

        cover_file = request.files.get(

            "cover_upload"

        )

        cover_url = request.form[

            "cover_url"

        ]

        if cover_file and cover_file.filename != "":

            upload_folder = os.path.join(
                app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(
                upload_folder,
                cover_file.filename
            )

            cover_file.save(filepath)

            cover_url = "/static/uploads/" + cover_file.filename

        # δημιουργια νεου βιβλιου

        copies = int(

            request.form["copies"]

        )

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

                request.form.getlist(

                    "categories"

                )

            ),

            cover_url=cover_url,

            copies=copies,

            total_copies=copies

        )

        db.session.add(

            book

        )

        db.session.commit()

        return redirect(

            "/books"

        )

    return render_template(

        "add_book.html"

    )


# λιστα βιβλιων και φιλτρα

@app.route("/books")
def books():

    search = request.args.get(

        "search",

        ""

    )

    categories = request.args.getlist(

        "categories"

    )

    language = request.args.get(

        "language",

        ""

    )

    year = request.args.get(

        "year",

        ""

    )

    pages = request.args.get(

        "pages",

        ""

    )

    available_only = request.args.get(

        "available_only"

    )

    # αρχικο query

    query = Book.query

    # αναζητηση

    if search:

        query = query.filter(

            (Book.title.ilike(

                f"%{search}%"

            )) |

            (Book.authors.ilike(

                f"%{search}%"

            ))

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

    book = Book.query.get_or_404(

        id

    )

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

    book = Book.query.get_or_404(

        id

    )

    if request.method == "POST":

        new_isbn = request.form["isbn"]

        cover_file = request.files.get(

            "cover_upload"

        )

        cover_url = request.form[

            "cover_url"

        ]

        # ελεγχος για νεα εικονα

        if cover_file and cover_file.filename != "":

            filepath = os.path.join(

                "static",

                "uploads",

                cover_file.filename

            )

            cover_file.save(

                filepath

            )

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

            request.form.getlist(

                "categories"

            )

        )

        book.cover_url = cover_url

        # ενημερωση αντιτυπων

        new_total = int(

            request.form["copies"] or 1

        )

        borrowed = (

            book.total_copies -

            book.copies

        )

        # δεν μπορει να μειωθει κατω απο τα δανεισμενα

        if new_total < borrowed:

            flash(

                "Δεν μπορειτε να ορισετε λιγοτερα αντιτυπα απο οσα ειναι ηδη δανεισμενα.",

                "danger"

            )

            return redirect(

                url_for(

                    "edit_book",

                    id=book.id

                )

            )

        book.total_copies = new_total

        book.copies = (

            new_total -

            borrowed

        )

        if book.copies > 0:

            book.status = "Available"

        else:

            book.status = "Borrowed"

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

    book = Book.query.get_or_404(

        id

    )

    # ελεγχος για ενεργο δανεισμο

    active_loan = Loan.query.filter_by(

        book_id=book.id,

        status="Borrowed"

    ).first()

    if active_loan:

        flash(

            "Δεν μπορείτε να διαγράψετε βιβλίο που είναι δανεισμένο.",

            "danger"

        )

        return redirect(

            url_for(

                "book_info",

                id=book.id

            )

        )

    db.session.delete(

        book

    )

    db.session.commit()

    flash(

        "Το βιβλίο διαγράφηκε επιτυχώς.",

        "success"

    )

    return redirect(

        url_for(

            "books"

        )

    )


#------------------- μελη -------------------


# λιστα μελων

@app.route("/members")
def members():

    search = request.args.get(

        "search",

        ""

    )

    query = Member.query

    # αναζητηση

    if search:

        query = query.filter(

            (Member.card_number.ilike(

                f"%{search}%"

            )) |

            (Member.first_name.ilike(

                f"%{search}%"

            )) |

            (Member.last_name.ilike(

                f"%{search}%"

            )) |

            ((

                Member.first_name +

                " " +

                Member.last_name

            ).ilike(

                f"%{search}%"

            ))

        )

    members = query.all()

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

    # ευρεση τελευταιου μελους

    last_member = Member.query.order_by(

        Member.id.desc()

    ).first()

    # δημιουργια νεου αριθμου καρτας

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

        db.session.add(

            member

        )

        db.session.commit()

        return redirect(

            "/members"

        )

    return render_template(

        "add_member.html",

        next_card_number=next_card_number

    )


# επεξεργασια μελους

@app.route(
    "/edit-member/<int:id>",
    methods=["GET", "POST"]
)
def edit_member(id):

    member = Member.query.get_or_404(

        id

    )

    if request.method == "POST":

        member.first_name = request.form[

            "first_name"

        ]

        member.last_name = request.form[

            "last_name"

        ]

        member.phone = request.form[

            "phone"

        ]

        member.date_of_birth = datetime.strptime(

            request.form[

                "date_of_birth"

            ],

            "%Y-%m-%d"

        ).date()

        member.address = request.form[

            "address"

        ]

        db.session.commit()

        flash(

            "Το μέλος ενημερώθηκε επιτυχώς.",

            "success"

        )

        return redirect(

            url_for(

                "member_info",

                id=member.id

            )

        )

    return render_template(

        "edit_member.html",

        member=member

    )


# διαγραφη μελους

@app.route(
    "/delete-member/<int:id>"
)
def delete_member(id):

    member = Member.query.get_or_404(

        id

    )

    # ελεγχος για ενεργους δανεισμους

    active_loans = Loan.query.filter_by(

        member_id=member.id,

        status="Borrowed"

    ).count()

    if active_loans > 0:

        return """

        <script>

        alert(

            'Δεν μπορεί να διαγραφεί μέλος με ενεργούς δανεισμούς.'

        );

        history.back();

        </script>

        """

    db.session.delete(

        member

    )

    db.session.commit()

    return redirect(

        url_for(

            "members"

        )

    )


#------------------- δανεισμοι -------------------


# σελιδα δανεισμων

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


# αποθηκευση δανεισμου

@app.route(
    "/save-loan",
    methods=["POST"]
)
def save_loan():

    data = request.get_json()

    # αναζητηση μελους

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

    # ελεγχος οριου δανεισμων

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

    # δημιουργια δανεισμων

    for isbn in data["books"]:

        book = Book.query.filter_by(

            isbn=isbn

        ).first()

        if not book:

            continue

        if book.copies <= 0:

            continue

        book.copies -= 1

        if book.copies == 0:

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


#------------------- επιστροφες -------------------


# σελιδα επιστροφων

@app.route(
    "/returns"
)
def returns():

    search = request.args.get(

        "search",

        ""

    )

    query = Loan.query.filter_by(

        status="Borrowed"

    )

    # αναζητηση

    if search:

        query = query.join(

            Member

        ).join(

            Book

        ).filter(

            (Member.card_number.ilike(

                f"%{search}%"

            )) |

            (Member.first_name.ilike(

                f"%{search}%"

            )) |

            (Member.last_name.ilike(

                f"%{search}%"

            )) |

            (Book.isbn.ilike(

                f"%{search}%"

            )) |

            (Book.title.ilike(

                f"%{search}%"

            ))

        )

    loans = query.all()

    return render_template(

        "returns.html",

        loans=loans,

        today=datetime.today().date()

    )


# επιστροφη βιβλιου

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

    today = datetime.today().date()

    # ενημερωση δανεισμου

    loan.status = "Returned"

    loan.return_date = today

    # ενημερωση αντιτυπων

    book.copies += 1

    book.status = "Available"

    # υπολογισμος χρεωσης

    if (

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

    db.session.commit()

    update_member_balance(

        loan.member_id

    )

    return redirect(

        url_for(

            "returns"

        )

    )


# εξοφληση χρεωσης

@app.route(
    "/pay-loan/<int:loan_id>"
)
def pay_loan(loan_id):

    loan = Loan.query.get_or_404(

        loan_id

    )

    if not loan.paid:

        loan.paid = True

        db.session.commit()

        update_member_balance(

            loan.member_id

        )

    return redirect(

        url_for(

            "member_info",

            id=loan.member_id

        )

    )


#------------------- εκκινηση εφαρμογης -------------------


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(

        debug=True

    )