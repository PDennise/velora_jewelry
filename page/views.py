from django.shortcuts import render
from django.http import Http404


def custom_404(request, exception):
    return render(request, "404.html", status=404)

def info_page(request, page):
    pages = {
        "about": {
            "template": "page/about.html",
            "banner_image": "/static/assets/images/about-img.png",
            "title": "About",
        },
        "contact": {
            "template": "page/contact.html",
            "banner_image": "/static/assets/images/contact-img.jpg",
            "title": "Contact Us",
        },
        "faq": {
            "template": "page/faq.html",
            "banner_image": "/static/assets/images/faq-img.png",
            "title": "FAQ",
        },
        "returns": {
            "template": "page/returns.html",
            "banner_image": "/static/assets/images/returns-img.png",
            "title": "Returns & Exchanges",
        },
        "shipping": {
            "template": "page/shipping.html",
            "banner_image": "/static/assets/images/shipping-img.png",
            "title": "Shipping & Delivery",
        },
        "size-guide": {
            "template": "page/size_guide.html",
            "banner_image": "/static/assets/images/sizeguide-img.png",
            "title": "Size Guide",
        },
    }

    if page not in pages:
        raise Http404()

    page_data = pages[page]

    return render(
        request,
        page_data["template"],
        {
            "banner_image": page_data["banner_image"],
        }
    )