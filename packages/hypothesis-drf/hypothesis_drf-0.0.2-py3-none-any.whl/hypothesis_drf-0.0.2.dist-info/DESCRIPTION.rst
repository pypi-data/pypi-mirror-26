[Hypothesis](https://github.com/HypothesisWorks/hypothesis-python) strategy for 
[Django REST framework](http://www.django-rest-framework.org/).


### Known issues

* `URLField` can be slow when generating the first example
* Not all fields are supported, known non-working:
  - FileField
  - FilePathField
  - ImageField
  - ModelField
  - JSONField(allow_null=False)


### Example

```
import json
from hypothesis_drf import from_serializer, from_field
from rest_framework import serializers


class ExampleSerializer(serializers.Serializer):
  name = serializers.CharField(min_length=3, max_length=8)
  amount = serializers.IntegerField(min_value=200, max_value=500)


from_serializer(ExampleSerializer).example()
# {'amount': 391, 'name': '\U00053a6b&\U00030fee$.'}

from_field(serializers.FloatField(min_value=-10, max_value=22)
# -8.499125311228873

```


### Custom fields

Provide `hypothesis_strategy` on the field:

```
from rest_framework import fields
from hypothesis import strategies as st

class MyField(fields.Field):
    hypothesis_strategy = st.booleans()

    # ...
```


