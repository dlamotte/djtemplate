from django.contrib.auth.models import User
from django.db import models
from django.db.models import get_model, signals
from tastypie.models import create_api_key

# Create your models here.


# signals
signals.post_save.connect(create_api_key, sender=User)
