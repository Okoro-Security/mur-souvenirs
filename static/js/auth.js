// =========================================================
// RÃ‰CUPÃ‰RER LE COOKIE CSRF
// =========================================================

function getCookie(name) {

    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {

        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {

            return decodeURIComponent(
                cookie.substring(name.length + 1)
            );
        }
    }

    return null;
}


// =========================================================
// CONNEXION
// =========================================================

const loginForm = document.getElementById("login-form");

if (loginForm) {

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username =
            document.getElementById("username").value.trim();

        const password =
            document.getElementById("password").value;

        const message =
            document.getElementById("login-message");

        const csrftoken =
            getCookie("csrftoken");


        if (!csrftoken) {

            message.textContent =
                "Erreur de sÃ©curitÃ©. Recharge la page.";

            message.style.color = "red";

            return;
        }


        try {

            const response = await fetch(
                "/api/login/",
                {
                    method: "POST",

                    credentials: "same-origin",

                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrftoken
                    },

                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                }
            );


            const data = await response.json();


            if (response.ok) {

                message.textContent =
                    "Connexion rÃ©ussie âœ…";

                message.style.color = "green";


                setTimeout(function () {

                    window.location.href = "/";

                }, 800);

            } else {

                message.textContent = data.detail || data.message || "Erreur de connexion."; 

                message.style.color = "red";
            }


        } catch (error) {

            console.error(error);

            message.textContent =
                "Erreur lors de la connexion.";

            message.style.color = "red";
        }

    });

}


// =========================================================
// INSCRIPTION
// =========================================================

const registerForm =
    document.getElementById("register-form");

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const username =
                document.getElementById("username").value.trim();

            const firstName =
                document.getElementById("first_name").value.trim();

            const lastName =
                document.getElementById("last_name").value.trim();

            const email =
                document.getElementById("email").value.trim();

            const niveau =
                document.getElementById("niveau").value;

            const promotion =
                document.getElementById("promotion").value.trim();

            const password =
                document.getElementById("password").value;

            const passwordConfirm =
                document.getElementById(
                    "password_confirm"
                ).value;

            const message =
                document.getElementById(
                    "register-message"
                );


            // -------------------------------------------------
            // VÃ©rification des mots de passe
            // -------------------------------------------------

            if (password !== passwordConfirm) {

                message.textContent =
                    "Les mots de passe ne correspondent pas.";

                message.style.color = "red";

                return;
            }


            const csrftoken =
                getCookie("csrftoken");


            if (!csrftoken) {

                message.textContent =
                    "Erreur de sÃ©curitÃ©. Recharge la page.";

                message.style.color = "red";

                return;
            }


            try {

                const response = await fetch(
                    "/api/register/",
                    {
                        method: "POST",

                        credentials: "same-origin",

                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrftoken
                        },

                        body: JSON.stringify({

                            username: username,

                            first_name: firstName,

                            last_name: lastName,

                            email: email,

                            password: password,

                            niveau: niveau,

                            promotion: promotion

                        })
                    }
                );


                const data =
                    await response.json();


                if (response.ok) {

                    message.textContent =
                        "Compte crÃ©Ã© avec succÃ¨s âœ…";

                    message.style.color = "green";


                    registerForm.reset();


                    setTimeout(function () {

                        window.location.href =
                            "/login/";

                    }, 1200);


                } else {

                    let erreur = "Erreur lors de l'inscription.";

                    if (data.username) {
                        erreur =
                            "Nom d'utilisateur : " +
                            data.username.join(" ");
                    }

                    else if (data.password) {
                        erreur =
                            "Mot de passe : " +
                            data.password.join(" ");
                    }

                    else if (data.niveau) {
                        erreur =
                            "Niveau : " +
                            data.niveau.join(" ");
                    }

                    else if (data.promotion) {
                        erreur =
                            "Promotion : " +
                            data.promotion.join(" ");
                    }

                    message.textContent = erreur;

                    message.style.color = "red";
                }


            } catch (error) {

                console.error(error);

                message.textContent =
                    "Erreur lors de la communication avec Django.";

                message.style.color = "red";
            }

        }
    );
}
