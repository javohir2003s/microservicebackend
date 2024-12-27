from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=150)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    photo = serializers.ImageField()
    description = serializers.CharField()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Narx musbat bo'lishi kerak.")
        return value