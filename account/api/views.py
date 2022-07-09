from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
# from django.conf import settings
from account.resources import InvitationResource
from tablib import Dataset



from account.api.serializers import NewAccountSerializer, UpdateUserSerializer, CreateEventSerializer, UpdateEventSerializer, UserEventsSerializer, CreateInvitationSerializer, EventInvitationsSerializer, UpdateInvitationSerializer, ScanInvitationSerializer
from account.models import Event, Invitation

from account.functions import send_confirmation_email

# Update Event
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_account(request):
    user = request.user
    
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
    
    if request.method == "POST":
        print(request.data)
        serializer = CreateEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
    
    return Response(serializer.data)


# Update Event
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer = UpdateEventSerializer(event, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "update successful"
            return Response(data=data)
        
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





# Get all events for user
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
def create_invitation(request):
    
    if request.method == "POST":
        serializer = CreateInvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
    
    return Response(serializer.data)



# Get all Invitations for Event
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def all_event_invitations(request, pk):
    event = Event.objects.get(id=pk)
    invitations = event.invitation_set.all()
    serializer = EventInvitationsSerializer(invitations, many=True)
    return Response(serializer.data)



# Update Invitation for Event (cleaned)
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_invitation(request, pk):

    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer = UpdateInvitationSerializer(invitation, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Invitation updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['error'] = "Somthing went wrong!"
            data['details'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)


# Update Invitation for Event (cleaned)
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
    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        operation = invitation.delete()
        data = {}
        if operation:
            data['success'] = "delete successful"
            # stat = status.HTTP_200_OK

        else:
            data["failure"] = "delete failed"
            # stat = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data)



# Get all Invitations for Event
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def confirmation_email(request, pk):
    user = request.user
    invitation_filtered = Invitation.objects.filter(id=pk)
    invitation = invitation_filtered.first()
    data = {}

    if invitation.status == "pending":
        invitation_filtered.update(status="waiting")
        send_confirmation_email(user.first_name, invitation.name, invitation.email, invitation.reference)
        data['success'] = "email sent"
        request_status = status.status.HTTP_200_OK
    else:
        data['error'] = "You have already send a confirmation email to this invitee!"
        request_status = status.HTTP_400_BAD_REQUEST

    return Response(data, status=request_status)



# Accept Invitation
def accept_invitation(request, pk):
    
    try:
        invitation = Invitation.objects.filter(reference=pk)
        if invitation.first().status == "waiting":
            invitation.update(status="confirmed")
            return HttpResponse("<h1>Invitation has been accepted!</h1>")
        else:
            return HttpResponse("<h1>This link has been used already!</h1>")

    except:
        return HttpResponse("<h1>Something went wrong!</h1>")


# Reject Invitation
def reject_invitation(request, pk):
    
    try:
        invitation = Invitation.objects.filter(reference=pk)
        if invitation.first().status == "waiting":
            invitation.update(status="apologized")
            return HttpResponse("<h1>Invitation has been rejected!</h1>")
        else:
            return HttpResponse("<h1>This link has been used already!</h1>")

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
