from django.shortcuts import render


def gameplay(request):
    return render(request, 'editions/gameplay.html')


def rules(request):
    return render(request, 'editions/rules.html')
