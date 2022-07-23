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
        fields = ['mobile', 'first_name', 'last_name']


class CreateEventSerializer(ModelSerializer):
    class Meta:

        model = Event
        fields = '__all__'
        read_only_fields = ['user']


class UpdateEventSerializer(ModelSerializer):
    class Meta:

        model = Event
        fields = ['name', 'venue', 'location', 'city', 'country', 'date']


class UserEventsSerializer(ModelSerializer):

    no_invitations = serializers.SerializerMethodField('number_of_invitations')
    pending = serializers.SerializerMethodField('pendings')
    waiting = serializers.SerializerMethodField('waitings')
    confirmed = serializers.SerializerMethodField('confirmeds')
    canceled = serializers.SerializerMethodField('canceleds')
    checked = serializers.SerializerMethodField('checkeds')

    class Meta:
        model = Event
        fields = ['id', 'user', 'name', 'venue', 'location', 'city', 'country', 'date', 'capacity', 'no_invitations','image', 'pending', 'waiting', 'confirmed', 'canceled', 'checked']
    
    def number_of_invitations(self, Event):
        invitations = Event.invitation_set.all()
        return invitations.count()
    
    
    def pendings(self, Event):
        pending = Event.invitation_set.filter(status="pending")
        return pending.count()

    def waitings(self, Event):
        waiting = Event.invitation_set.filter(status="waiting")
        return waiting.count()
    
    def confirmeds(self, Event):
        confirmed = Event.invitation_set.filter(status="confirmed")
        return confirmed.count()
    
    def canceleds(self, Event):
        canceled = Event.invitation_set.filter(status="apologized")
        return canceled.count()

    def checkeds(self, Event):
        checked = Event.invitation_set.filter(status="checked")
        return checked.count()
    

    

class CreateInvitationSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['event', 'first_name', 'last_name', 'mobile', 'email']
        read_only_fields = ['event']

        

# Get General Statistics
class GetGeneralStatisticsSerializer(serializers.Serializer):
    pending = serializers.IntegerField()
    



# Get all invitation for one event 
class EventInvitationsSerializer(ModelSerializer):

    class Meta:
        model = Invitation
        fields = ['id', 'event', 'first_name', 'last_name', 'mobile', 'email', 'status']








class UpdateInvitationSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['name', 'mobile', 'email', 'status']


class UpdateInvitationStatusSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['status']




class ScanInvitationSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['status']


