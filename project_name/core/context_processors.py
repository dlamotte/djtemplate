from django.conf import settings
from {{ project_name }}.core.apiv1 import UserResource

def default(request):
    user = 'null'
    res_user = UserResource()
    if hasattr(request, 'user') and request.user.is_authenticated():
        user = res_user.serialize(
            None,
            res_user.full_dehydrate(res_user.build_bundle(obj=request.user)),
            'application/json'
        )

    return {
        'user_json': user,
        'settings': settings,
    }
