from django.shortcuts import render

# Create your views here.
def hello(request):
    html_page = 'hello.html'
    return render(request,html_page)