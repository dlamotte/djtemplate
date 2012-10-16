from django.db.models import get_model
from tastypie.api import Api
from tastypie.resources import ModelResource

api = Api(api_name='v1')

class UserResource(ModelResource):
    class Meta:
        queryset = get_model('auth', 'User').objects.all()
        exclude = ('password', )
api.register(UserResource())
