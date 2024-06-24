from rest_framework import serializers

class ExampleSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.IntegerField()
    # Define other fields as per your data structure