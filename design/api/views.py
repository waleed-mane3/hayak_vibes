from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
# from django.conf import settings

from design.api.serializers import AllDesignsSerializer
from design.models import Design

from design.resources import CardResource
from django.shortcuts import render
from tablib import Dataset



# Get all Designs
@api_view(['GET',])
# @permission_classes([IsAuthenticated])
def get_all_designs(request):
    designs = Design.objects.all()
    serializer = AllDesignsSerializer(designs, many=True)
    return Response(serializer.data)



# Test Card
@api_view(['GET',])
# @permission_classes([IsAuthenticated])
def card_view(request):
    designs = Design.objects.all()
    serializer = AllDesignsSerializer(designs, many=True)
    return Response(serializer.data)



def export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        employee_resource = CardResource()
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



def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = CardResource()
        dataset = Dataset()
        new_employees = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='csv')
            result = employee_resource.import_data(dataset, dry_run=True)                                                                 
        elif file_format == 'JSON':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='json')
            # Testing data import
            result = employee_resource.import_data(dataset, dry_run=True)
        elif file_format == 'XLS':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='XLS')
            # Testing data import
            result = employee_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            # Import now
            employee_resource.import_data(dataset, dry_run=False)

    return render(request, 'design/import.html')  