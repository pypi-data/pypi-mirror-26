[Hypothesis](https://github.com/HypothesisWorks/hypothesis-python) strategy for 
[Django REST framework](http://www.django-rest-framework.org/) serializers.


Generate data that is valid according to a DRF serializer

### Known issues

* Only tested with python3.6
* `URLField` can be slow when generating the first example
* `*RelatedField` gets first object in queryset, not random
* Not all fields are supported, known non-working:
    - FileField
    - FilePathField
    - ImageField
    - HyperlinkedModelSerializer
    - ModelSerializer
    - ModelField


### Example

```bash
pip install hypothesis-drf
```

```python
from hypothesis_drf import from_serializer, from_field
from rest_framework import serializers


class ExampleSerializer(serializers.Serializer):
  name = serializers.CharField(min_length=3, max_length=8)
  amount = serializers.IntegerField(min_value=200, max_value=500)


from_serializer(ExampleSerializer).example()
# {'amount': 391, 'name': '\U00053a6b&\U00030fee$.'}

from_field(serializers.FloatField(min_value=-10, max_value=22)).example()
# -8.499125311228873

```


For HyperLinkedRelatedField (and variants) you must pass an instantiated serializer as
they require access to the request via context:

```python
from hypothesis_drf import from_serializer

class RelatedExample(serializers.ModelSerializer):
    class Meta:
        model = SourceModel
        fields = ('target', )

    target = HyperLinkedRelatedField(queryset=TargetModel.objects.all())

from_serializer(RelatedExample(context={'request': request})).example()
# {'target': 'http://example.com/something/'}
```


### Custom fields

Provide `hypothesis_strategy` on the field:

```python
from rest_framework import fields
from hypothesis import strategies as st

class MyField(fields.Field):
    hypothesis_strategy = st.booleans()

    # ...
```


