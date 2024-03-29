from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserCreatePasswordRetypeSerializer 
from rest_framework import serializers
from .models import Space, UserAccess, User
from django.db import transaction



class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class SpaceSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)
    @transaction.atomic
    def save(self, **kwargs):
        space = super().save(**kwargs)
        current_user = self.context.get('request', None).user


        try:
            user_access = UserAccess.objects.get(space_id = space.id, user_id = current_user.id)
            user_access.save()
        except UserAccess.DoesNotExist:
            user_access = UserAccess.objects.create(user_id = current_user.id, space_id = space.id)
            user_access.save()
        
        space.owner_id = current_user.id
        space.save()
        # User.objects.update(id = current_user.id, current_space_id = space.id)
        return space
    
    class Meta:
        model = Space
        fields = ['id', 'code', 'title', 'owner']

class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
    current_space = SpaceSerializer()
    spaces = SpaceSerializer(many = True)
    class Meta(BaseUserSerializer.Meta):
        fields= ['id', 'username', 'email', 'first_name', 'last_name', 'current_space', 'spaces', 'is_active']

class UserAccessSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only = True)
    # space = SpaceSerializer(read_only = True)
    class Meta:
        model = UserAccess
        fields = ['id', 'user', 'space']

class SpaceListSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer()
    # user_count = serializers.SerializerMethodField()
    members_number = serializers.IntegerField(source='users.count', read_only=True)
    # def get_user_count(self, obj):
    #     return obj.user_set.count() + 1
    class Meta:
        model = Space
        fields = ['id', 'code', 'title', 'last_modification_date', 'owner', 'members_number'] 




class AddSpaceAccessToUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.EmailField()
    def validate_user_id(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'No user with the given email was found.')
        return value

    def save(self, **kwargs):
        space_id = self.context['space_id']
        user = User.objects.get(email = self.validated_data['user_id'])
        user_id = user.id
        if not user.is_active:
            raise serializers.ValidationError('This user is not active')
        try:
            user_access = UserAccess.objects.get(space_id = space_id, user_id = user_id)
            user_access.save()
            self.instance = user_access
        except UserAccess.DoesNotExist:
            self.instance = UserAccess.objects.create(user_id = user_id, space_id = space_id)

        # User.objects.filter(pk=user_id).update(current_space_id=space_id)
        return self.instance

    class Meta:
        model = UserAccess
        fields = ['id', 'user_id']




