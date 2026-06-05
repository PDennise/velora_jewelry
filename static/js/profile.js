document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // CSRF TOKEN (secure method)
    // =========================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCookie('csrftoken');


    // =========================
    // PHONE UPDATE
    // =========================
    const saveButton = document.getElementById("save-profile-btn");

    if (saveButton) {
        saveButton.addEventListener("click", function () {

            const phone = document.getElementById("phone-input").value;

            fetch(updatePhoneUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    phone: phone
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {

                    // UI update
                    document.getElementById("phone-display").textContent = data.phone;

                    // modal close
                    const modalEl = document.getElementById("editProfileModal");
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    modal?.hide();

                    showBanner("Contact Info Updated");
                }
            })
            .catch(err => console.error(err));

        });
    }


    // =========================
    // EDIT ADDRESS
    // =========================
    const saveAddressBtn = document.getElementById("save-address-btn");

    if (saveAddressBtn) {
        saveAddressBtn.addEventListener("click", function () {

            fetch(updateProfileUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    street_address1: document.getElementById("address1-input").value,
                    street_address2: document.getElementById("address2-input").value,
                    city: document.getElementById("city-input").value,
                    county: document.getElementById("county-input").value,
                    postcode: document.getElementById("postcode-input").value
                })
            })
            .then(res => res.json())
            .then(data => {

                if (data.success) {

                    const modalEl =
                        document.getElementById("editAddressModal");

                    const modal =
                        bootstrap.Modal.getInstance(modalEl);

                    modal?.hide();

                    showBanner("Address Updated");
                    location.reload();
                }

            })
            .catch(err => console.error(err));
        });
    }


    // =========================
    // BANNER
    // =========================
    function showBanner(message) {
        const banner = document.createElement("div");
        banner.className = "alert alert-success position-fixed top-0 start-50 translate-middle-x mt-3";
        banner.style.zIndex = "9999";
        banner.innerText = message;

        document.body.appendChild(banner);

        setTimeout(() => {
            banner.remove();
        }, 2500);
    }

});