from django.shortcuts import render

# Create your views here.
def main_page(request):
    response = render(request, 'main.html')
    return response