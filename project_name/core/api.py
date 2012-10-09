from django.db.models import get_model
from tastypie.api import Api
from tastypie.resources import ModelResource

# minor improvements on ApiKeyAuthentication from tastypie to allow for
# specifying crendtials in the headers also
class ApiKeyAuthentication(object):
    """
    Handles API key auth, in which a user provides a username & API key.

    Uses the ``ApiKey`` model that ships with tastypie. If you wish to use
    a different model, override the ``get_key`` method to perform the key check
    as suits your needs.
    """
    def _get_credentials(self, request):
        username = request.GET.get('username') or request.POST.get('username')
        api_key = request.GET.get('api_key') or request.POST.get('api_key')

        if not username or not api_key:
            authorization = request.META.get('HTTP_AUTHORIZATION', '')
            try:
                kind, creds = authorization.split()
            except ValueError:
                pass
            else:
                if kind == 'ApiKey':
                    try:
                        username, api_key = creds.split(':')
                    except ValueError:
                        pass

        return username, api_key

    def _unauthorized(self):
        return HttpUnauthorized()

    def is_authenticated(self, request, **kwargs):
        """
        Finds the user and checks their API key.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """
        from django.contrib.auth.models import User

        username, api_key = self._get_credentials(request)

        if not username or not api_key:
            return self._unauthorized()

        try:
            user = User.objects.get(username=username)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return self._unauthorized()

        request.user = user
        return self.get_key(user, api_key)

    def get_key(self, user, api_key):
        """
        Attempts to find the API key for the user. Uses ``ApiKey`` by default
        but can be overridden.
        """
        from tastypie.models import ApiKey

        try:
            ApiKey.objects.get(user=user, key=api_key)
        except ApiKey.DoesNotExist:
            return self._unauthorized()

        return True

    def get_identifier(self, request):
        """
        Provides a unique string identifier for the requestor.

        This implementation returns the user's username.
        """
        username, api_key = self._get_credentials(request)
        return username or 'nouser'

api = Api(api_name='v1')

class UserResource(ModelResource):
    class Meta:
        queryset = get_model('auth', 'User').objects.all()
        exclude = ('password', )
api.register(UserResource())
