from django.shortcuts import render
from .forms import ImageForm

# Create your views here.
def hello(request):
    imageForm = ImageForm(request.POST or None, request.FILES or None)
    if imageForm.is_valid():
        f =imageForm.save(commit=False)
        img = f.image
        print(img)
    else:
        imageForm = ImageForm()
    
    html_page = 'hello.html'
    return render(request,html_page,{'imageForm':imageForm})