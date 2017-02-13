from django.shortcuts import render


# Create your views here.

def index(request) -> str:
    """
    Display start page.

    :param request:
    :return:
    """
    return render(request, 'welcome/index.html')
