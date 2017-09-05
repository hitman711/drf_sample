""" Permission classes list
  TenantAuthentication
"""
from rest_framework import authentication
from rest_framework import exceptions
from . import models

class TenantAuthentication(authentication.BaseAuthentication):
    """ Authentication against user access level
    """
    def authenticate(self, request):
        """ Authenticate tenant API_KEY & update API hits.
        """
        tenant = models.Tenant.objects.filter(
            api_key=request.GET.get('api_key')
        ).last()
        if not tenant:
            raise exceptions.AuthenticationFailed('Invalid API key')
        tenant.update_api_hit()
