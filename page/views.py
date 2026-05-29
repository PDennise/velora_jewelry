from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'page/about.html')

def contact(request):
    return render(request, 'page/contact.html')

def shipping(request):
    return render(request, 'page/shipping.html')

def returns(request):
    return render(request, 'page/returns.html')

def faq(request):
    return render(request, 'page/faq.html')

def size_guide(request):
    return render(request, 'page/size_guide.html')