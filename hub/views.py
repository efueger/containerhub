from django.shortcuts import render, redirect
from django.conf import settings

from .models import Container


# Create your views here.

def dashboard(request):
    """

    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return render(request, 'hub/dashboard.html')
    else:
        return redirect('welcome:login')


def profile(request, user_id: int = None):
    """
    Display users profile page.

    :param request:
    :return:
    """
    if user_id:
        user = settings.AUTH_USER_MODEL.objects.get(user_id)
    else:
        user = request.user

    context = {user:  user}
    return render(request, 'hub/profile.html', context)


def list_containers(request):
    """
    List containers you have access to

    :param request:
    :return:
    """
    current_user = request.user
    containers = Container.objects.filter(owner=current_user)

    context = {containers: containers}
    return render(request, 'hub/containers.html', context)


# TODO: user sshkey: if startswith('###invalid###') display error message
