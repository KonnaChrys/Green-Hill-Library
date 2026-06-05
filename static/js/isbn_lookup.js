async function lookupISBN() {

    const isbn = document.getElementById("isbn").value;

    if (!isbn) {
        alert("Δώσε ISBN");
        return;
    }

    try {

        const response = await fetch(
            `https://openlibrary.org/isbn/${isbn}.json`
        );

        if (!response.ok) {
            alert("Το βιβλίο δεν βρέθηκε");
            return;
        }

        const data = await response.json();

        document.getElementById("title").value =
            data.title || "";

        document.getElementById("publisher").value =
            data.publishers ?
            data.publishers[0] :
            "";

        document.getElementById("year").value =
            data.publish_date ?
            data.publish_date.match(/\d{4}/)?.[0] || "" :
            "";

        document.getElementById("cover").src =
            `https://covers.openlibrary.org/b/isbn/${isbn}-L.jpg`;

    }

    catch(error) {

        console.error(error);

        alert("Σφάλμα σύνδεσης");

    }

}