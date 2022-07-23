from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
# from django.conf import settings
from account.resources import InvitationResource
from tablib import Dataset

from account.api.serializers import (
    NewAccountSerializer, 
    UpdateUserSerializer, 
    CreateEventSerializer, 
    UpdateEventSerializer, 
    UserEventsSerializer, 
    CreateInvitationSerializer, 
    EventInvitationsSerializer, 
    UpdateInvitationSerializer, 
    ScanInvitationSerializer,
    GetGeneralStatisticsSerializer,
    UpdateInvitationStatusSerializer
)
from account.models import Event, Invitation

from account.functions import send_confirmation_email
from utils.functions import send_email
import json


# Update Event
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_account(request):
    user = request.user
    data = {}

    if request.method == "PUT":
        serializer = UpdateUserSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "update successful"
            return Response(data=data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST',])
def new_account_view(request):
    
    if request.method == 'POST':
        serializer = NewAccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Successfully created new account!"
            data['email'] = account.email
            data['fullname'] = f"{account.first_name} {account.last_name}" 
            stat = status.HTTP_201_CREATED
        else:
            # data = serializer.errors
            data['response'] = serializer.errors
            stat = status.HTTP_400_BAD_REQUEST
            
            # status=status.HTTP_400_BAD_REQUEST
        
        return Response(data, status=stat)
            
            

# Create New Event for user 
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def create_event(request):
    user = request.user
    data = {}

    serializer = CreateEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        data['success'] = "You have created new event successfully!"
        request_status = status.HTTP_201_CREATED
    else:
        data['error'] = serializer.errors
        request_status = status.HTTP_400_BAD_REQUEST 
            
    return Response(data=data, status=request_status)
      



# Update Event (VIBES)
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    data = {}

    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        data['error'] = "This Event is not existed with this id!"
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)
    
    serializer = UpdateEventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        request_status = status.HTTP_200_OK
        data['success'] = "Event has been updated successfully!"
    else:
        request_status = status.HTTP_400_BAD_REQUEST
        data['error'] = serializer.errors
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete Event
@api_view(['DELETE',])
@permission_classes([IsAuthenticated])
def delete_event(request, pk):
    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        operation = event.delete()
        data = {}
        if operation:
            data['success'] = "delete successful"
            # stat = status.HTTP_200_OK

        else:
            data["failure"] = "delete failed"
            # stat = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data)





# Get all events for user (VIBES)
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def all_user_events(request):
    user = request.user
    events = user.event_set.all()
    serializer = UserEventsSerializer(events, many=True)
    return Response(serializer.data)



# Create New Invitation for Event 
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def create_invitation(request, pk):
    data = {}

    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        data['error'] = "This event is not existed with this id!"
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)
    
    serializer = CreateInvitationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(event=event)
        data['success'] = "You have created new invitation successfully!"
        request_status = status.HTTP_201_CREATED

    else:
        data['error'] = serializer.errors
        request_status = status.HTTP_400_BAD_REQUEST 
            
    return Response(data=data, status=request_status)
    




# Get all Invitations for Event
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def all_event_invitations(request, pk):
    data = {}

    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        data['error'] = "This event is not existed with this id!"
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)

    invitations = event.invitation_set.all()
    serializer = EventInvitationsSerializer(invitations, many=True)
    


    data = serializer.data
    request_status = status.HTTP_200_OK

    return Response(data=data, status=request_status)


# Update Invitation for Event 
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_invitation(request, pk):
    data = {}

    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        data['error'] = "This invitation is not existed with this id!"
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)
    
    serializer = UpdateInvitationStatusSerializer(invitation, data=request.data)
    if serializer.is_valid():
        serializer.save()
        data['success'] = "Invitation updated successfully!"
        request_status = status.HTTP_200_OK

    else:
        data['error'] = serializer.errors
        request_status = status.HTTP_400_BAD_REQUEST
    
    return Response(data=data, status=request_status)


# Update Invitation for Event 
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_status(request, pk):
    data = {}
    chosen_status = request.data['status']

    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        data['error'] = "This invitation is not existed with this id!"
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)
    
    serializer = UpdateInvitationStatusSerializer(invitation, data=request.data)
    if serializer.is_valid():

        if invitation.status == "pending":
            if chosen_status == "pending": 
                data['error'] = "This invitation is already in pending status!"
                request_status = status.HTTP_200_OK

            if chosen_status == "rejected": 
                serializer.save()
                # rejected_email(invitation.email, invitation.first_name)
                data['success'] = "Invitation has been updated successfully!"
                data['status'] = "rejected"
                request_status = status.HTTP_200_OK

            elif chosen_status == "accepted":
                serializer.save() 
                # accepted_email(invitation.email, invitation.first_name, reference_no)
                data['success'] = "Invitation has been updated successfully!"
                data['status'] = "accepted"
                request_status = status.HTTP_200_OK

            # ??
            elif chosen_status == "confirmed": 
                # accepted_email(invitation.email, invitation.first_name, reference_no)
                data['error'] = "you cannot confirm invitation with pending status!"
                request_status = status.HTTP_400_BAD_REQUEST
        
        if invitation.status == "rejected":
            if chosen_status == "pending": 
                data['error'] = "You cannot change this status to pending!"
                request_status = status.HTTP_400_BAD_REQUEST

            if chosen_status == "rejected": 
                data['error'] = "this invitation has been rejected already!"
                request_status = status.HTTP_400_BAD_REQUEST

            elif chosen_status == "accepted":
                data['error'] = "this invitation has been rejected already!"
                request_status = status.HTTP_400_BAD_REQUEST

            # ??
            elif chosen_status == "confirmed": 
                data['error'] = "You cannot confirm rejected invitation!"
                request_status = status.HTTP_400_BAD_REQUEST
            
        if invitation.status == "accepted":
            if chosen_status == "pending": 
                data['error'] = "You cannot change this status to pending!"
                request_status = status.HTTP_400_BAD_REQUEST

            if chosen_status == "rejected": 
                data['error'] = "This invitation has been accepted already!"
                request_status = status.HTTP_400_BAD_REQUEST

            elif chosen_status == "accepted":
                data['error'] = "This invitation has been accepted already!"
                request_status = status.HTTP_400_BAD_REQUEST

            # ??
            elif chosen_status == "confirmed": 
                serializer.save() 
                # confirmed_email(invitation.email, invitation.first_name)
                data['success'] = "Invitation has been updated successfully!"
                data['status'] = "confirmed"
                request_status = status.HTTP_200_OK
            
        if invitation.status == "confirmed":
            if chosen_status == "pending" or chosen_status == "rejected" or chosen_status == "accepted": 
                data['error'] = "You cannot change this status to confirmed!"
                request_status = status.HTTP_400_BAD_REQUEST

            elif chosen_status == "confirmed": 
                data['error'] = "This invitation has been confirmed already!"
                request_status = status.HTTP_400_BAD_REQUEST
        

    else:
        data['error'] = serializer.errors
        request_status = status.HTTP_400_BAD_REQUEST
    
    return Response(data=data, status=request_status)


# Scan Invitation
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def scan_invitation(request, pk):
    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data_to_update = {'status': 'checked'}
    if request.method == "PUT":
        serializer = ScanInvitationSerializer(invitation, data=data_to_update)
        print(serializer)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data['success'] = "Invitation Scanned successful!"
            request_status = status.HTTP_200_OK
        else:
            data['error'] = "Scanning went wrong!"
            data['details'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)




# Delete Invitation for Event
@api_view(['DELETE',])
@permission_classes([IsAuthenticated])
def delete_invitation(request, pk):
    data = {}

    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        data['error'] = "This invitation is not existed with this id!"
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)
    
    operation = invitation.delete()
    if operation:
        data['success'] = "Invitation has been deleted successfully!"
        request_status = status.HTTP_200_OK

    else:
        data["failure"] = "Deletion failed!"
        request_status = status.HTTP_501_NOT_IMPLEMENTED

    return Response(data=data, status=request_status)


# Confirm Email
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def confirmation_email(request, pk):
    user = request.user
    invitation_filtered = Invitation.objects.filter(id=pk)
    invitation = invitation_filtered.first()
    data = {}

    if invitation.status == "pending":
        invitation_filtered.update(status="waiting")
        send_email(invitation.email, invitation.first_name, invitation.reference, "confirm")
        data['success'] = "confirmation email sent successfully!"
        request_status = status.HTTP_200_OK
    else:
        data['error'] = "You have already sent a confirmation email to this invitee!"
        request_status = status.HTTP_400_BAD_REQUEST

    return Response(data, status=request_status)



# Accept Invitation
def accept_invitation(request, pk):
    invitation = Invitation.objects.filter(reference=pk)
    print(invitation)
    try:
        filtered_invitation = Invitation.objects.filter(reference=pk)
        invitation = filtered_invitation.first()
        if invitation.status == "waiting":
            send_email(invitation.email, invitation.first_name, invitation.reference, "accept")
            filtered_invitation.update(status="confirmed")
            return render(request, 'account/thanks.html')
        else:
            return render(request, 'account/confirmed.html')

    except:
        return HttpResponse("<h1>Something went wrong!</h1>")


# Reject Invitation
def reject_invitation(request, pk):
    
    try:
        filtered_invitation = Invitation.objects.filter(reference=pk)
        invitation = filtered_invitation.first()
        if invitation.status == "waiting":
            send_email(invitation.email, invitation.first_name, invitation.reference, "reject")
            filtered_invitation.update(status="apologized")
            return render(request, 'account/thanks.html')
        else:
            return render(request, 'account/confirmed.html')

    except:
        return HttpResponse("<h1>Something went wrong!</h1>")
    




def export_guests(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        employee_resource = InvitationResource()
        dataset = employee_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   

    return render(request, 'design/export.html')



@api_view(['POST',])
# @permission_classes([IsAuthenticated])
def import_guests(request, pk):
    data = {}
    
    event = Event.objects.get(id=pk)
    event_capacity = event.capacity
    print(f"Event Capacity: {event_capacity}")

    current_invitations = event.invitation_set.all().count()
    print(f"Current Invitations: {current_invitations}")

    allowed = event_capacity - current_invitations
    print(f"Allowed to Add: {allowed}")


    
    if request.method == 'POST':
        file_format = 'CSV'
        invitations_resource = InvitationResource()
        dataset = Dataset()
        new_guests = request.FILES['file']

        if file_format == 'CSV':
            imported_data = dataset.load(new_guests.read().decode('utf-8'),format='csv')
            dataset_count = len(dataset)
            event_list_ids = [int(pk)] * dataset_count
            dataset.append_col(event_list_ids, header='event')
            
            if dataset_count <= allowed:
                result = invitations_resource.import_data(dataset, dry_run=True) 
                data['success'] = "Import has been done successfully!"
                request_status = status.HTTP_200_OK

            else:
                data['error'] = "your imported file exceeded your package invitations"
                data['allowed'] = allowed
                request_status = status.HTTP_400_BAD_REQUEST

        if dataset_count <= allowed:
            if not result.has_errors():
                # Import now
                invitations_resource.import_data(dataset, dry_run=False)
    

    return Response(data=data, status=request_status)  
