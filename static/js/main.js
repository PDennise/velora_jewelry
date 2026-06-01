document.addEventListener("DOMContentLoaded", function () {

    const navbar = document.getElementById("mainNavbar");

    window.addEventListener("scroll", () => {

        console.log(window.scrollY);

        if (window.scrollY > 80) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }

    });
})

document.addEventListener("DOMContentLoaded", function () {

    const featuredSlider = document.querySelector('.featured-slider');

    if(featuredSlider){

        new Flickity(featuredSlider, {

            cellAlign: 'left',

            contain: false,

            wrapAround: true,

            autoPlay: 3000,

            pauseAutoPlayOnHover: true,

            selectedAttraction: 0.04,

            friction: 0.45,

            prevNextButtons: true,

            pageDots: true,

            percentPosition: false,
            
            resize: true,
            
            imagesLoaded: true,

        });

    }
});

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("newsletterBtn");
    const input = document.getElementById("newsletterEmail");
    const msg = document.getElementById("newsletterMsg");

    if (btn) {
        btn.addEventListener("click", function () {
            const email = input.value.trim();

            if (!email || !email.includes("@")) {
                msg.textContent = "Please enter a valid email address.";
                msg.className = "newsletter-msg error";
                return;
            }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            fetch('/newsletter/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: `email=${encodeURIComponent(email)}`
            })
            .then(res => res.json())
            .then(data => {
                msg.textContent = data.message;
                msg.className = `newsletter-msg ${data.status}`;
                if (data.status === 'success') input.value = '';
            })
            .catch(() => {
                msg.textContent = 'Something went wrong. Please try again.';
                msg.className = 'newsletter-msg error';
            });
        });
    }
});

function removeEmptyParams(form) {
    Array.from(form.elements).forEach(el => {
        if (el.type === "checkbox") return; // checkbox'ları atla, value="1" olduğu için disable olmasın
        if (!el.value) el.disabled = true;
    });
}


// for quantity 

function changeQty(delta) {
    const input = document.getElementById('quantity');
    if (!input) return;  // sadece bu satır ekstra
    const max = parseInt(input.max);
    let val = parseInt(input.value) + delta;
    if (val < 1) val = 1;
    if (val > max) val = max;
    input.value = val;
}