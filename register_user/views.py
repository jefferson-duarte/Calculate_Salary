from django.shortcuts import render


def teste(request):
    return render(
        request,
        'auth/pages/index.html'
    )
