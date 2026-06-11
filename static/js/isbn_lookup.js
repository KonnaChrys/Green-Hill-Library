async function lookupISBN() {

    const isbn = document.getElementById("isbn").value;

    if (!isbn) {

        alert("Δωσε ISBN");

        return;

    }

    try {

        // αναζητηση βιβλιου

        const response = await fetch(
            `https://openlibrary.org/isbn/${isbn}.json`
        );

        if (!response.ok) {

            alert("Το βιβλιο δεν βρεθηκε");

            return;

        }

        const data = await response.json();


        // τιτλος

        document.getElementById("title").value =
            data.title || "";


        // εκδοτης

        document.getElementById("publisher").value =
            data.publishers ?
            data.publishers[0] :
            "";


        // γλωσσα
        // μεταφραση του language key στα ελληνικα

        if (data.languages && data.languages.length > 0) {

            const languageResponse = await fetch(
                `https://openlibrary.org${data.languages[0].key}.json`
            );

            const languageData =
                await languageResponse.json();

            const languageMap = {

                "English": "Αγγλικα",

                "French": "Γαλλικα",

                "German": "Γερμανικα",

                "Italian": "Ιταλικα",

                "Spanish": "Ισπανικα",

                "Greek": "Ελληνικα"

            };

            document.getElementById("language").value =
                languageMap[languageData.name] ||
                languageData.name;

        }


        // ετος και σελιδες

        document.getElementById("year").value =
            data.publish_date ?
            data.publish_date.match(/\d{4}/)?.[0] || "" :
            "";

        document.querySelector('[name="pages"]').value =
            data.number_of_pages || "";


        // επιπλεον στοιχεια βιβλιου
        // το isbn endpoint δεν περιεχει παντα ολες τις πληροφοριες

        if (data.works && data.works.length > 0) {

            const workResponse = await fetch(
                `https://openlibrary.org${data.works[0].key}.json`
            );

            const workData =
                await workResponse.json();


            // συγγραφεας

            if (workData.authors &&
                workData.authors.length > 0) {

                let authors = [];

                for (const author of workData.authors) {

                    const authorResponse =
                        await fetch(
                            `https://openlibrary.org${author.author.key}.json`
                        );

                    const authorData =
                        await authorResponse.json();

                    authors.push(authorData.name);

                }

                document.getElementById("authors").value =
                    authors.join(", ");

            }


            // κατηγοριες

            const tom =
                document.getElementById(
                    "categories"
                ).tomselect;

            // αφαιρεση προηγουμενων επιλογων

            tom.clear();

            // αντιστοιχιση κατηγοριων openlibrary

            const categoryMap = {

                "Fantasy": "Fantasy",

                "Adventure": "Adventure",

                "Science fiction": "Sci-fi",

                "Science Fiction": "Sci-fi",

                "Sci-fi": "Sci-fi",

                "Mystery": "Mystery",

                "Thriller": "Thriller",

                "Romance": "Romance",

                "Horror": "Horror",

                "Historical fiction":
                    "Historical Fiction",

                "History": "History",

                "Biography": "Biography",

                "Autobiography":
                    "Autobiography",

                "Poetry": "Poetry",

                "Psychology": "Psychology",

                "Philosophy": "Philosophy",

                "Business": "Business",

                "Politics": "Politics",

                "Religion": "Religion",

                "Science": "Science",

                "Technology": "Technology",

                "Programming":
                    "Programming",

                "Children": "Children",

                "Young adult":
                    "Young Adult",

                "Comics": "Comics"

            };

            if (workData.subjects) {

                workData.subjects.forEach(
                    subject => {

                        if (
                            categoryMap[subject]
                        ) {

                            tom.addItem(
                                categoryMap[subject]
                            );

                        }

                    }
                );

            }


            // περιληψη
            // μπορει να επιστραφει ως string η object

            if (workData.description) {

                if (
                    typeof workData.description
                    === "string"
                ) {

                    document.getElementById(
                        "description"
                    ).value =
                        workData.description;

                }

                else {

                    document.getElementById(
                        "description"
                    ).value =
                        workData.description.value
                        || "";

                }

            }

        }


        // τυπος εξωφυλλου

        const coverTypeMap = {

            "paperback":
                "Μαλακο εξωφυλλο",

            "hardcover":
                "Σκληρο εξωφυλλο"

        };

        document.getElementById(
            "cover_type"
        ).value =
            coverTypeMap[
                data.physical_format
                ?.toLowerCase()
            ] ||
            data.physical_format ||
            "";


        // εξωφυλλο

        if (
            data.covers &&
            data.covers.length > 0
        ) {

            const cover =
                document.getElementById(
                    "cover"
                );

            cover.src =
                `https://covers.openlibrary.org/b/id/${data.covers[0]}-L.jpg`;

            document.getElementById(
                "cover_url"
            ).value =
                cover.src;

            cover.style.display =
                "block";

            document.getElementById(
                "cover_placeholder"
            ).style.display =
                "none";

            document.getElementById(
                "cover_container"
            ).style.border =
                "none";

        }

        else {

            // εμφανιση placeholder αν δεν υπαρχει εξωφυλλο

            document.getElementById(
                "cover"
            ).style.display =
                "none";

            document.getElementById(
                "cover_placeholder"
            ).style.display =
                "block";

            document.getElementById(
                "cover_container"
            ).style.border =
                "1px solid #ccc";

        }

    }

    catch (error) {

        console.error(error);

        alert(error);

    }

}