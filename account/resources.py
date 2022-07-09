from import_export import resources
from account.models import Invitation 

class InvitationResource(resources.ModelResource):
    class Meta:
        model = Invitation