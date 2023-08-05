from django.contrib.auth.models import User
from django.db.models import BinaryField
from django.db.models import DateTimeField
from django.db.models import FloatField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import TextField
from django.db.models import Model

class RequestProfile(Model):
    started_at = DateTimeField()
    created_at = DateTimeField()
    request_user = ForeignKey(User, null=True)
    request_path = TextField(blank=True)
    response_code = IntegerField()
    time_real = FloatField()
    time_user = FloatField()
    time_sys = FloatField()
    allocated_vm = IntegerField()
    data = BinaryField(null=True)
