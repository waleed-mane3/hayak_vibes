from django.urls import path
from account.api.views import (
    new_account_view, 
    update_account, 
    create_event, 
    update_event, 
    delete_event, 
    all_user_events, 
    create_invitation, 
    all_event_invitations, 
    update_invitation, 
    delete_invitation, 
    confirmation_email, 
    accept_invitation, 
    reject_invitation, 
    scan_invitation,
    export_guests,
    import_guests,
    update_status
)

app_name = 'account'

urlpatterns = [
    # Users
    path('new_account/', new_account_view, name='new_account_view'),
    path('update_account/', update_account, name='update_user'),
    # Events 
    # path('create_event/', create_event),
    path('update_event/<str:pk>/', update_event),
    # path('delete_event/<str:pk>/', delete_event),
    path('user_events/', all_user_events),
    # Invitations
    path('create_invitation/<str:pk>/', create_invitation),
    path('event_invitations/<str:pk>/', all_event_invitations),
    path('update_invitation/<str:pk>/', update_invitation),
    path('invitation/update-status/<str:pk>/', update_status),
    path('scan_invitation/<str:pk>/', scan_invitation),
    path('delete_invitation/<str:pk>/', delete_invitation),
    # path('export_guests/', export_guests, name='export_guests'),
    path('import_guests/<str:pk>/', import_guests, name='import_guests'),
    # Confirming Invitation
    path('accept_invitation/<str:pk>/', accept_invitation),
    path('reject_invitation/<str:pk>/', reject_invitation),
    # Emails
    path('confirmation_email/<str:pk>/', confirmation_email),
    # others
    # path('overview/', overview),
]

 