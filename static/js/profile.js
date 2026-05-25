document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.getElementById("save-profile-btn");

    if (saveButton) {
        saveButton.addEventListener("click", function () {
            const phone = document.getElementById("phone-input").value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

            fetch(updateProfileUrl, {
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
                    document.getElementById("phone-display").textContent = data.phone;

                    const modal = bootstrap.Modal.getInstance(
                        document.getElementById("editProfileModal")
                    );
                    modal.hide();
                }
            });
        });
    }
});