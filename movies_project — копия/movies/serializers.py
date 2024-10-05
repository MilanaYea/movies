from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'director', 'length', 'rating']
        extra_kwargs = {
            'id': {'required': True, 'allow_null': False}
        }

    def validate_year(self, value):
        if value < 1900 or value > 2100:
            raise serializers.ValidationError("Field 'year' should be between 1900 and 2100")
        return value

    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Field 'rating' should be between 0 and 10")
        return value