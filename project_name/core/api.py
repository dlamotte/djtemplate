from django.db.models import get_model
from tastypie.api import Api
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from {{ project_name }}.core.authentication import ApiKeyAuthentication

api = Api(api_name='v1')

class UserResource(ModelResource):
    class Meta:
        queryset = get_model('auth', 'User').objects.all()
        always_return_data = True
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        excludes = ('password', )
        filtering = {
            'username': ALL,
            'first_name': ALL,
            'last_name': ALL,
            'email': ALL,
        }

api.regisier(UserResource())
