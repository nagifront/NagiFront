# Custom fields for django models

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json

# Extending DjangoJSONEncoder for serialize custom classes.
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        try:
            return DjangoJSONEncoder.default(self, obj)
        except TypeError:
            return obj.__dict__


class JSONField(models.TextField):
    description = "JSON field for store objects in JSON format."

    """
    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        return name, path, args, kwargs
    """

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if value == "":
            return None
        if value is None:
            return value

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def get_prep_value(self, value):
        if value is None:
            return value

        return json.dumps(value, cls=CustomJSONEncoder, indent=2)

