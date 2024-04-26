import secrets
import string

from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect


class OrganizerRoleCheckerAndLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizer:
            return redirect("leads")
        return super().dispatch(request, *args, **kwargs)


class CustomRawPasswordGenerator:
    def generateRawPassword(self):
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        return password


class RedirectIfAlreadyLoggedInMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)
