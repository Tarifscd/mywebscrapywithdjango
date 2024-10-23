from rest_framework import serializers

class ScrapyDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    data_type = serializers.CharField(max_length=15, required=False)
    path = serializers.CharField(max_length=300, required=False)
    published_date = serializers.DateField(required=False)