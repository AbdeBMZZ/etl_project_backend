from rest_framework import serializers
from .models import CSVFile, TransformationRule, TransformedData

class CSVFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = '__all__'

class TransformationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformationRule
        fields = '__all__'

class TransformedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformedData
        fields = '__all__'

