from django.shortcuts import render


# Create your views here.
def learning_index(request):
    return render(request, 'index.html', {})
