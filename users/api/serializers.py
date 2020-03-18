from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()

class CurrentUserDetailSerializer(serializers.ModelSerializer):
    screen_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username','screen_name','img_profile'
        ]

    def get_screen_name(self,obj):
        return obj.profile.screen_name()

    def get_profile_picture(self,obj):
        request = self.context.get('request')
        profile_picture_url = obj.profile.get_picture()
        return request.build_absolute_uri(profile_picture_url)

class UserDetailSerializer(serializers.ModelSerializer):
    screen_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'screen_name','username'
        ]

    def get_screen_name(self,obj):
        return obj.profile.screen_name()

class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True,read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'email','password','token'
        ]
        extra_kwargs = {
            "password":{
                "write_only":True
            }
        }
    
    def validate(self,data):
        username = data['username']
        email = data['email']
        password = data['password']
        user_qs = User.objects.filter(
            Q(username__iexact=username) | 
            Q(email__iexact=email)
        ).distinct()
        if user_qs.exists() and user_qs.count() == 1:
            user_obj = user_qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                data['token'] = token
            else:
                raise serializers.ValidationError("Incorrect password")
        else:
            raise serializers.ValidationError("The user with this username does not exists")
        return data

class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self,obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = [
            'token','username','email','password',
        ]

class ProfileRetrieveSerailizer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    screen_name = serializers.SerializerMethodField()
    requester_in_contact_list = serializers.SerializerMethodField()
    requester_in_pending_list = serializers.SerializerMethodField()
    has_followed = serializers.SerializerMethodField()
    is_requesters_profile = serializers.SerializerMethodField()
    created_groups_count = serializers.SerializerMethodField()
    posted_posts_count = serializers.SerializerMethodField()
    groups_subsribed_count = serializers.SerializerMethodField()
    member_since = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'profile_image_url','screen_name','requested_in_contact_list',
            'requested_in_pending_list','has_followed','is_requesters_profile',
            'created_groups_count','posted_posts_count','groups_subscribed_count',
            'member_since',
        ]

    def get_profile_image_url(self,obj):
        request = self.context.get['request']
        profile_image_url = obj.profile.get_picture()
        return request.build_absolute_url(profile_image_url)

    def get_screen_name(self,obj):
        return obj.profile.screen_name()

    def get_requested_in_contact_list(self,obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request,'user'):
            user = request.user
        if user in obj.profile.contact_list.all():
            return True
        return False

    def get_requested_in_pending_list(self,obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request,'user'):
            user = request.user
        if user in obj.profile.pending_list.all():
            return True
        return False

    def get_is_requesters_profile(self,obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request,'user'):
            user = request.user
        if user == obj:
            return True
        return False
    
    def get_has_followed(self,obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request,'user'):
            user = request.user
        if user in obj.profile.followers.all():
            return True
        return False

    def get_created_groups_count(self,obj):
        return obj.inspected_groups.count()

    def get_posted_posts_count(self,obj):
        return obj.posted_posts.count()

    def get_groups_subscribed_count(self,obj):
        return obj.subscribed_groups.count()

    def get_member_since(self,obj):
        return obj.profile.member_since.date()