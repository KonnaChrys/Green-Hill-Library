async function lookupISBN() {

    const isbn = document.getElementById("isbn").value;

    if (!isbn) {
        alert("Δώσε ISBN");
        return;
    }

    try {

        // ΑΝΑΖΗΤΗΣΗ ΒΙΒΛΙΟΥ

        const response = await fetch(
            `https://openlibrary.org/isbn/${isbn}.json`
        );

        if (!response.ok) {
            alert("Το βιβλίο δεν βρέθηκε");
            return;
        }


        const data = await response.json();
        console.log(data);//προσορινο
        console.log(data.contributors);//προσορινο


        // ΤΙΤΛΟΣ

        document.getElementById("title").value =
            data.title || "";



        // ΕΚΔΟΤΗΣ

        document.getElementById("publisher").value =
            data.publishers ?
            data.publishers[0] :
            "";


        // ΓΛΩΣΣΑ
        // μεταφραζω το language key στα ελληνικα

        if (data.languages && data.languages.length > 0) {

            const languageResponse = await fetch(
                `https://openlibrary.org${data.languages[0].key}.json`
            );

            const languageData = await languageResponse.json();

            const languageMap = {

                "English": "Αγγλικά",

                "French": "Γαλλικά",

                "German": "Γερμανικά",

                "Italian": "Ιταλικά",

                "Spanish": "Ισπανικά",

                "Greek": "Ελληνικά"

            };

            document.getElementById("language").value =
                languageMap[languageData.name] || languageData.name;
        }


        // ΕΤΟΣ / ΣΕΛΙΔΕΣ

        document.getElementById("year").value =
            data.publish_date ?
            data.publish_date.match(/\d{4}/)?.[0] || "" :
            "";

        document.querySelector('[name="pages"]').value =
            data.number_of_pages || "";


        // WORK DATA(Περιληψη/Κατηγοριες)
        // το ISBN endpoint δεν έχει παντα τις πληροφορίες, γι' αυτο κανω δευτερο fetch στο work endpoint

        if (data.works && data.works.length > 0) {

            const workResponse = await fetch(
                `https://openlibrary.org${data.works[0].key}.json`
            );

            const workData = await workResponse.json();

            // ΣΥΓΓΡΑΦΕΑΣ

            if (workData.authors && workData.authors.length > 0) {

                let authors = [];

                for (const author of workData.authors) {

                    const authorResponse = await fetch(
                        `https://openlibrary.org${author.author.key}.json`
                    );

                    const authorData = await authorResponse.json();

                    authors.push(authorData.name);

                }

                document.getElementById("authors").value =
                    authors.join(", ");

            }

            // ΚΑΤΗΓΟΡΙΕΣ

            const tom =
                document.getElementById("categories").tomselect;

            // καθαριζω προηγουμενες επιλογες

            tom.clear();

            // αντιστοιχιση κατηγοριων OpenLibrary με δικες μου

            const categoryMap = {

                "Fantasy": "Fantasy",

                "Adventure": "Adventure",

                "Science fiction": "Sci-fi",

                "Science Fiction": "Sci-fi",

                "Sci-fi": "Sci-fi",

                "Mystery": "Mystery",

                "Thriller": "Thriller",

                "Romance": "Romance",

                "Horror": "Horror"

            };

            if (workData.subjects) {

                workData.subjects.forEach(subject => {

                    if (categoryMap[subject]) {

                        tom.addItem(categoryMap[subject]);

                    }

                });

            }



            // ΠΕΡΙΛΗΨΗ
            // μερικες φορες ειναι string και αλλες object

            if (workData.description) {

                if (typeof workData.description === "string") {

                    document.getElementById("description").value =
                        workData.description;

                }

                else {

                    document.getElementById("description").value =
                        workData.description.value || "";

                }

            }

        }

        // ΤΥΠΟΣ ΕΞΩΦΥΛΛΟΥ


        const coverTypeMap = {

            "paperback": "Μαλακό εξώφυλλο",

            "hardcover": "Σκληρό εξώφυλλο"

        };

        document.getElementById("cover_type").value =
            coverTypeMap[data.physical_format?.toLowerCase()] ||
            data.physical_format ||
            "";

        // ΕΞΩΦΥΛΛΟ

        if (data.covers && data.covers.length > 0) {

            const cover = document.getElementById("cover");

            cover.src =
                `https://covers.openlibrary.org/b/id/${data.covers[0]}-L.jpg`;

            document.getElementById("cover_url").value =
                cover.src;

            cover.style.display = "block";

            document.getElementById("cover_placeholder").style.display =
                "none";

            document.getElementById("cover_container").style.border =
                "none";

        }

        else {

            // αν δεν βρεθει εξωφυλλο εμφανισε placeholder

            document.getElementById("cover").style.display =
                "none";

            document.getElementById("cover_placeholder").style.display =
                "block";

            document.getElementById("cover_container").style.border =
                "1px solid #ccc";

        }

    }

    catch(error) {

        console.error(error);

        alert(error);

    }

}