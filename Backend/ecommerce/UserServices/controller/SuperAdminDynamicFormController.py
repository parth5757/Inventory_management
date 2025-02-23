import json
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ecommerce.Helpers import getExcludeFields, renderResponse, getSuperAdminDynamicFormModels
from ecommerce.permission import IsSuperAdmin
from rest_framework.response import Response
from rest_framework import status
from django.core.serializers import serialize

class SuperAdminDynamicFormController(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    
    def post(self, request, modelName):

        # checking our Model is exist in our Dynamic form Models

        if modelName not in getSuperAdminDynamicFormModels():
            return renderResponse(data='Model Not Exist', message='Model Not Exist', status=status.HTTP_400_BAD_REQUEST)
            
        # Getting the model Name from Dynamic Models
        model = getSuperAdminDynamicFormModels() [modelName]
        model_class = apps.get_model(model)
    
        # Getting the model class from Dynamic odels
        if model_class is None:
            return Response ({'error': 'Model not found'}, status=404)
        
        # getting model fields
        fields_info = model_class._meta.fields
        # getting model fields name
        model_fields = {field.name for field in fields_info}
        # getting model fields excluded
        excluded_fields = getExcludeFields()

        # checking if required data fields are in Model data
        required_fields = [field.name for field in fields_info if not field.null and field.default is not None and field.name not in excluded_fields]

        # matching with validation for fields not exist in post data
        missing_field = [field  for field in required_fields if field not in request.data]
    
        # make exit while any missing fields
        if missing_field:
            return Response({"error": [f'This field is required :{field}' for field in missing_field]}, status=400)
        
        # Create a copy of post data for manipulation
        fields = request.data.copy()

        # filtering post data fields by Model Fields and eliminating the extra fields

        fieldsdata={key:value for key, value in fields.items() if key in model_fields}
        # print(model_fields)
        # print(fields.items())
        # print(fieldsdata.items())

        #Assigning Foreign key instance for ForeignKey Fields in the Post Data by getting the instance of the related model by the ID
        for field in fields_info:
            if field.is_relation and field.name in fieldsdata and isinstance(fieldsdata[field.name],int):
                related_model=field.related_model
                try:
                    fieldsdata[field.name]=related_model.objects.get(id=fieldsdata[field.name])
                except related_model.DoesNotExist:
                    return Response(data=f'{field.name} Relation Not Exist found',status=404)

        # creating model instance to save data
        model_instance = model_class.objects.create(**fieldsdata)
        
        # Serializing data
        serialized_data = serialize('json', [model_instance])
        # converting serialized data to json
        model_json = json.loads(serialized_data) 
        # getting first object in json
        response_json = model_json[0]['fields']
        response_json['id'] = model_json[0]['pk']
        return Response({'data': response_json, 'message':'data save successfully'})    