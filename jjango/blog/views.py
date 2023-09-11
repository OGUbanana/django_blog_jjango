from django.shortcuts import render

# Create your views here.
def index(request):
    print('board')
    return render(request, 'board.html')