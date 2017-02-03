import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login


from social_core.backends.utils import load_backends
from social_django.models import UserSocialAuth
from social_django.utils import psa, load_strategy

from .decorators import render_to


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


@render_to('home.html')
def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')


def emails(request):
    instance = UserSocialAuth.objects.filter(provider='google-oauth2')
    _emails = []
    for x in instance:
        _emails.append(x.uid)
    context = {'emails_list': _emails}
    return render(request, 'emails.html', context)


@login_required
@render_to('home.html')
def done(request):
    """Login complete view, displays user data"""
    pass


@render_to('home.html')
def validation_sent(request):
    """Email validation sent confirmation page"""
    return {
        'validation_sent': True,
        'email': request.session.get('email_validation_address')
    }


@render_to('home.html')
def require_email(request):
    """Email required page"""
    strategy = load_strategy()
    partial_token = request.GET.get('partial_token')
    partial = strategy.partial_load(partial_token)
    return {
        'email_required': True,
        'partial_backend_name': partial.backend,
        'partial_token': partial_token
    }
