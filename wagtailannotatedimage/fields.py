import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class AnnotationsField(models.TextField):
    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, dict):
            return value

        if value is None:
            return value

        try:
            return json.loads(value)
        except ValueError:
            return None

    def get_prep_value(self, value):
        return json.dumps(value, cls=DjangoJSONEncoder)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
