from django.shortcuts import render

def abrir_index(request):
    return render(request, 'index.html')