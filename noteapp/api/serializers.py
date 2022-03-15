from django.forms import CharField, DateField, FileField
from rest_framework.serializers import Serializer, ModelSerializer
from noteapp.models import User,Note,Profile
from rest_framework.serializers import *
from django.contrib.auth.models import User

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class SignupSer(Serializer):
    password=CharField(write_only=True,error_messages={'required':'password key is required','blank':'password  is required'})
    email=CharField(error_messages={'required':'email key is required','blank':'email is required'})
    username=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    first_name=CharField(error_messages={'required':False,'blank':True})
    last_name=CharField(error_messages={'required':False,'blank':True})

    def validate(self,data):
        username=data.get('username')
        qs=User.objects.filter(username=data.get('username'))
        if qs.exists():
            raise ValidationError("Username already exists")
        
        qs=User.objects.filter(email=data.get('email'))
        if qs.exists():
            raise ValidationError("Email already exists")
        return data

    def create(self,validated_data):
        obj=User.objects.create_user(username=validated_data.get('username'),email=validated_data.get('email'),first_name=validated_data.get('first_name'),last_name=validated_data.get('last_name'))
        obj.set_password(validated_data.get('password'))
        obj.save()
        return validated_data

class LoginSer(Serializer):
    username=CharField(error_messages={'required':'Email key is required','blank':'Email is required'})
    password=CharField(error_messages={'required':'Password key is required','blank':'Password is required'})
    token=CharField(read_only=True, required=False)

    def validate(self,data):
        qs=User.objects.filter(username=data.get('username'))
        if not qs.exists():
            raise ValidationError('No account with this username')
        user=qs.first()
        if user.check_password(data.get('password'))==False:
            raise ValidationError('Invalid Password')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data['token']='JWT'+str(token)
        return data

class NoteSer(Serializer):
    note_name=CharField(error_messages={'required':'name key is required','blank':False})
    description =CharField(error_messages={'required':'description key is required','blank':True})
    def create(self, data):
        Note.objects.create(u_id=self.context.get('user'),note_name=data.get('note_name'),description=data.get('description')).save()
        return data

class NoteSer1(Serializer):

    note_name=CharField(error_messages={'required':'name key is required','blank':False})
    description =CharField(error_messages={'required':'description key is required','blank':True})
    def update(self,instance,validated_data):
        instance.u_id=self.context.get('user')
        instance.note_name=validated_data.get('note_name')
        instance.description=validated_data.get('description')
        instance.save()
        return validated_data 

TITLE_CHOICES = [
    ('1', 'Normal_user'),
    ('2', 'Employee'),
    
]
 
class ProfileSer(ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'
        
   