from django.shortcuts import render

def index(request):
    return render(request, "pages/index.html", {"show_counter":"show_counter"})

def why(request):
    return render(request, "pages/why.html")

def about(request):
    return render(request, "pages/about.html")

def process(request):
    return render(request, "pages/process.html")

def bitcoin_api(request):
    pass