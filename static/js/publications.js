const API_URL = "/api/publications/";

function obtenirCookie(nom) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(nom + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(nom.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}

const publicationsContainer =
    document.getElementById("publications-container");

async function chargerPublications() {
    if (!publicationsContainer) {
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "GET",
            credentials: "same-origin",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}`);
        }

        const data = await response.json();
        const publications = data.results || data;

        afficherPublications(publications);

    } catch (error) {
        console.error("Erreur chargement publications :", error);

        publicationsContainer.innerHTML = `
            <div class="publication-card">
                <p>Impossible de charger les souvenirs.</p>
            </div>
        `;
    }
}

function afficherPublications(publications) {
    publicationsContainer.innerHTML = "";

    if (!publications || publications.length === 0) {
        publicationsContainer.innerHTML = `
            <div class="publication-card">
                <p>Aucun souvenir publié pour le moment.</p>
            </div>
        `;
        return;
    }

    publications.forEach(function (publication) {

        const article = document.createElement("article");
        article.className = "publication-card";

        const auteur = publication.auteur
            ? (
                publication.auteur.first_name ||
                publication.auteur.username ||
                "Utilisateur"
            )
            : "Utilisateur";

        const texteLike = publication.a_deja_like
            ? "?? Retirer le like"
            : "?? J'aime";

        let commentairesHTML = "";

        if (
            publication.commentaires &&
            publication.commentaires.length > 0
        ) {
            commentairesHTML = publication.commentaires
                .map(function (commentaire) {

                    const nomCommentaire =
                        commentaire.auteur
                            ? (
                                commentaire.auteur.first_name ||
                                commentaire.auteur.username ||
                                "Utilisateur"
                            )
                            : "Utilisateur";

                    return `
                        <div class="commentaire">
                            <strong>${nomCommentaire}</strong>
                            <p>${commentaire.texte}</p>
                        </div>
                    `;
                })
                .join("");
        } else {
            commentairesHTML = `
                <p>Aucun commentaire.</p>
            `;
        }

        let boutonSupprimer = "";

        if (publication.est_auteur) {
            boutonSupprimer = `
                <button
                    type="button"
                    class="delete-button"
                    onclick="supprimerPublication(${publication.id})"
                >
                    ??? Supprimer
                </button>
            `;
        }

        let imageHTML = "";

        if (publication.image) {
            imageHTML = `
                <img
                    src="${publication.image}"
                    class="publication-image"
                    alt="Souvenir"
                >
            `;
        }

        article.innerHTML = `
            <div class="publication-header">
                <strong>${auteur}</strong>

                <span>
                    ${publication.annee || ""}
                </span>
            </div>

            <div class="publication-type">
                ${publication.type || "Souvenir"}
            </div>

            <p class="publication-text">
                ${publication.texte || ""}
            </p>

            ${imageHTML}

            <div class="publication-actions">

                <button
                    type="button"
                    class="like-button"
                    onclick="aimerPublication(${publication.id})"
                >
                    ${texteLike}
                    (${publication.nombre_likes || 0})
                </button>

                <span>
                    ?? ${publication.nombre_commentaires || 0}
                </span>

            </div>

            <div class="commentaires-container">
                ${commentairesHTML}
            </div>

            <div class="comment-section">

                <input
                    type="text"
                    id="commentaire-${publication.id}"
                    class="comment-input"
                    placeholder="Écrire un commentaire..."
                >

                <button
                    type="button"
                    class="comment-button"
                    onclick="ajouterCommentaire(${publication.id})"
                >
                    Commenter
                </button>

            </div>

            ${boutonSupprimer}
        `;

        publicationsContainer.appendChild(article);
    });
}

async function supprimerPublication(publicationId) {

    const confirmation = confirm(
        "Es-tu sûr de vouloir supprimer cette publication ?"
    );

    if (!confirmation) {
        return;
    }

    try {
        const response = await fetch(
            `/api/publications/${publicationId}/`,
            {
                method: "DELETE",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": obtenirCookie("csrftoken")
                }
            }
        );

        if (response.status === 401) {
            alert("Tu dois être connecté.");
            return;
        }

        if (response.status === 403) {
            alert(
                "Tu ne peux supprimer que tes propres publications."
            );
            return;
        }

        if (!response.ok) {
            alert("Impossible de supprimer la publication.");
            return;
        }

        alert("Publication supprimée avec succès.");

        await chargerPublications();

    } catch (error) {
        console.error("Erreur suppression :", error);

        alert("Impossible de contacter le serveur.");
    }
}

async function aimerPublication(publicationId) {

    try {
        const response = await fetch(
            `/api/publications/${publicationId}/like/`,
            {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": obtenirCookie("csrftoken")
                }
            }
        );

        if (response.status === 401) {
            alert(
                "Tu dois être connecté pour aimer une publication."
            );
            return;
        }

        if (!response.ok) {
            alert("Erreur like HTTP " + response.status);
            return;
        }

        await response.json();

        await chargerPublications();

    } catch (error) {
        console.error("Erreur lors du like :", error);
    }
}

async function ajouterCommentaire(publicationId) {

    const input = document.getElementById(
        `commentaire-${publicationId}`
    );

    if (!input) {
        return;
    }

    const texte = input.value.trim();

    if (texte === "") {
        alert(
            "Écris un commentaire avant de publier."
        );
        return;
    }

    try {
        const response = await fetch(
            `/api/publications/${publicationId}/commentaires/`,
            {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-CSRFToken": obtenirCookie("csrftoken")
                },
                body: JSON.stringify({
                    texte: texte
                })
            }
        );

        if (response.status === 401) {
            alert(
                "Tu dois être connecté pour commenter."
            );
            return;
        }

        const data = await response.json();

        if (!response.ok) {
            console.error(
                "Erreur commentaire :",
                data
            );

            alert(
                "Impossible d'ajouter le commentaire."
            );
            return;
        }

        input.value = "";

        await chargerPublications();

    } catch (error) {
        console.error(
            "Erreur commentaire :",
            error
        );

        alert(
            "Impossible de contacter le serveur."
        );
    }
}

chargerPublications();

const publicationForm = document.getElementById("publication-form");

if (publicationForm) {
    publicationForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const message = document.getElementById("publication-message");
        const bouton = publicationForm.querySelector('button[type="submit"]');

        const formData = new FormData(publicationForm);
        const imageInput = document.getElementById("image");

        if (imageInput && imageInput.files.length > 0) {
            formData.set("image", imageInput.files[0]);
        }

        if (message) {
            message.textContent = "Publication en cours...";
        }

        if (bouton) {
            bouton.disabled = true;
        }

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "X-CSRFToken": obtenirCookie("csrftoken")
                },
                credentials: "same-origin",
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                console.error("Erreur publication :", data);

                if (message) {
                    message.textContent =
                        data.detail ||
                        "Impossible de publier le souvenir.";
                }

                return;
            }

            if (message) {
                message.textContent = "?? Souvenir publié avec succès !";
            }

            publicationForm.reset();

            await chargerPublications();

        } catch (error) {
            console.error("Erreur réseau :", error);

            if (message) {
                message.textContent =
                    "Une erreur est survenue. Vérifie ta connexion.";
            }

        } finally {
            if (bouton) {
                bouton.disabled = false;
            }
        }
    });
}


