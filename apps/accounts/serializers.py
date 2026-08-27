from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """Handles public signup. Only ever creates candidate accounts —
    staff/mentor/recruiter/admin accounts are created via the admin panel."""

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name", "phone"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data["role"] = "candidate"
        user = User(**validated_data)
        user.set_password(password)
        user.is_email_verified = False
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Used to represent a user in API responses (e.g. after login, or /me/)."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "full_name",
            "phone", "role", "is_email_verified", "date_joined",
        ]
        read_only_fields = fields


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()