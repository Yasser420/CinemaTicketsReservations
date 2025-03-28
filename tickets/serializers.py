from rest_framework import serializers
from .models import User , Reservation , Movie
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.db import IntegrityError

user = get_user_model()

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model= Movie
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True , validators=[validate_password])   
    passwordConfirm = serializers.CharField(write_only=True)
    class Meta : 
        model = User
        fields = ['username' , 'email' , 'password' , 'passwordConfirm']
        extra_kwargs = {
            'email': {'required':True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['passwordConfirm'] : 
            raise serializers.ValidationError('passwords are not match')
        attrs.pop('passwordConfirm', None)
        return attrs 
    def create(self, validated_data):
    
     try:
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
        )
        return user
    
     except Exception as e:
       return "error"
    def to_representation(self, res):
        # This method controls how the user data is represented when serialized
        user_data = super().to_representation(res)
        # Add all fields you want to return here
        user_data['id'] = res.id
        user_data['username'] = res.username
        user_data['email'] = res.email
        user_data['role'] = res.role  
        return user_data
    
class UserLoginSerializer(TokenObtainPairSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
   

    def validate(self, attrs):
        """Authenticate user with email, password, and role."""
        email = attrs.get("email")
        password = attrs.get("password")
        role = attrs.get("role")

        if not role:
            raise serializers.ValidationError("Role is required.")

        try:
            user = User.objects.get(email=email)

            # Validate password
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

            # Validate role
            if user.role != role:
                raise serializers.ValidationError("Please provide the correct role.")

        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        # Generate token using the correct email instead of username
        data = super().validate({"email": user.email, "password": password})
        data['username']=user.username
        data['email']=user.email
        data['role']=user.role
        data['userId']=user.pk
    
        return data
    

class AddAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'passwordConfirm']
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, attrs):
        if attrs['password'] != attrs['passwordConfirm'] : 
            raise serializers.ValidationError('passwords are not match')
        attrs.pop('passwordConfirm', None)
        return attrs 
    def create(self, validated_data):
        try:
            admin = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role='admin'  # Make sure your User model has this field
            )
            return admin
        except IntegrityError as e:
            raise serializers.ValidationError({"error": "User already exists"})
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})