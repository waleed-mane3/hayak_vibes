from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from auth_system.models import CustomUser
from django.contrib.auth import get_user_model
from account.models import Event, Invitation

# Register new account serializer
class NewAccountSerializer(serializers.ModelSerializer):
    
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model= get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}, #this will prevent users to read the password when it is passed through the request
        }
    
    def save(self):
        account = CustomUser(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email']
        )

        password = self.validated_data['password']

        # if password != password2:
        #     raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        account.set_password(password)
        account.save()
        return account
    
# This is used to update #first_sign_in# field
class UpdateUserSerializer(ModelSerializer):
    class Meta:

        model = CustomUser
        fields = ['id', 'first_name', 'first_sign_in', ]


class CreateEventSerializer(ModelSerializer):
    class Meta:

        model = Event
        fields = ['user', 'name', 'venue', 'groom', 'bride', 'date',]


class UpdateEventSerializer(ModelSerializer):
    class Meta:

        model = Event
        fields = ['name', 'venue', 'groom', 'bride', 'date']


class UserEventsSerializer(ModelSerializer):

    no_invitations = serializers.SerializerMethodField('number_of_invitations')

    class Meta:

        model = Event
        fields = ['id', 'user', 'name', 'venue', 'groom', 'bride', 'date', 'no_invitations']
    
    def number_of_invitations(self, Event):
        invitations = Event.invitation_set.all()
        return invitations.count()

    

class CreateInvitationSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['event', 'name', 'mobile', 'email']


# Get all invitation for one event 
class EventInvitationsSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['id', 'event', 'name', 'mobile', 'email', 'status']


class UpdateInvitationSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['name', 'mobile', 'email', 'status']
    

class ScanInvitationSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['status']







