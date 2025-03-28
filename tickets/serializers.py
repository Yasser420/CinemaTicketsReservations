from rest_framework import serializers
from .models import User , Reservation , Movie
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db import IntegrityError

user = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        exclude = ['password']
        

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model= Movie
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'

class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError("Password is wrong")

        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        data = super().validate({"email": user.email, "password": password})

        data['username'] = user.username
        data['email'] = user.email
        data['role'] = user.role  
        data['userId'] = user.pk

        return data
    
class BaseUserSerializer(serializers.ModelSerializer):
    passwordConfirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'passwordConfirm']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """Ensure passwords match and remove passwordConfirm."""
        if attrs['password'] != attrs['passwordConfirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        attrs.pop('passwordConfirm', None)
        return attrs

    def get_role(self):
        return 'user'  # Default role

    def create(self, validated_data):
        """Create a user with the provided role."""
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=self.get_role()  # Use the role from the child class
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError({"error": "User already exists."})
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        
class RegisterUserSerializer(BaseUserSerializer):
    """Serializer for user registration (default role: 'user')."""
    def get_role(self):
        return 'user'
            
class AddAdminSerializer(BaseUserSerializer):
    """Serializer for adding an admin (role: 'admin')."""
    def get_role(self):
        return 'admin'  
    
