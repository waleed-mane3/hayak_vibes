from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from auth_system.models import CustomUser
from account.models import Event, Invitation

    

# Get all Judging
class GetGeneralStatisticsSerializer(serializers.ModelSerializer):
    
    invitees = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()
    waiting = serializers.SerializerMethodField()
    confirmed = serializers.SerializerMethodField()
    canceled = serializers.SerializerMethodField()
    checked = serializers.SerializerMethodField()


    class Meta:
        model = Invitation
        fields = ('invitees', 'pending', 'waiting', 'confirmed', 'canceled', 'checked')

    def get_invitees(self, obj):
        return self.context.get("invitees")
    
    def get_pending(self, obj):
        return self.context.get("pending")
    
    def get_waiting(self, obj):
        return self.context.get("waiting")
    
    def get_confirmed(self, obj):
        return self.context.get("confirmed")
    
    def get_canceled(self, obj):
        return self.context.get("canceled")

    def get_checked(self, obj):
        return self.context.get("checked")

    

    










# # This is used to update #first_sign_in# field
# class UpdateUserSerializer(ModelSerializer):
#     class Meta:

#         model = CustomUser
#         fields = ['mobile', 'first_name', 'last_name']


# class CreateEventSerializer(ModelSerializer):
#     class Meta:

#         model = Event
#         fields = '__all__'
#         read_only_fields = ['user']


# class UpdateEventSerializer(ModelSerializer):
#     class Meta:

#         model = Event
#         fields = ['name', 'venue', 'location', 'city', 'country', 'date']


# class UserEventsSerializer(ModelSerializer):

#     no_invitations = serializers.SerializerMethodField('number_of_invitations')

#     class Meta:

#         model = Event
#         fields = ['id', 'user', 'name', 'venue', 'location', 'city', 'country', 'date', 'capacity', 'no_invitations', 'image']
    
#     def number_of_invitations(self, Event):
#         invitations = Event.invitation_set.all()
#         return invitations.count()

    

# class CreateInvitationSerializer(ModelSerializer):
#     class Meta:

#         model = Invitation
#         fields = ['event', 'first_name', 'last_name', 'mobile', 'email']
#         read_only_fields = ['event']


# # Get all invitation for one event 
# class EventInvitationsSerializer(ModelSerializer):
#     class Meta:

#         model = Invitation
#         fields = ['id', 'event', 'name', 'mobile', 'email', 'status']


# class UpdateInvitationSerializer(ModelSerializer):
#     class Meta:

#         model = Invitation
#         fields = ['name', 'mobile', 'email', 'status']
    

# class ScanInvitationSerializer(ModelSerializer):
#     class Meta:

#         model = Invitation
#         fields = ['status']







