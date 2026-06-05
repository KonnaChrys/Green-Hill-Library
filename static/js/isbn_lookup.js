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

        document.querySelector('[name="pages"]').value =
            data.number_of_pages || "";

        console.log(data);
        
        if (data.covers && data.covers.length > 0) {

            const cover = document.getElementById("cover");

            cover.src =
                `https://covers.openlibrary.org/b/id/${data.covers[0]}-L.jpg`;

            cover.style.display = "block";
        }

    }

    catch(error) {

        console.error(error);

        alert("Σφάλμα σύνδεσης");

    }

}