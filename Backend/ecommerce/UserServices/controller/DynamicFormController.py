# external imports
# rest framework libraries imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# django libraries imports  
from django.apps import apps
from django.core.serializers import serialize

# python libraries import
import json

# internal imports
# project internal file & function imports
from ecommerce.Helpers import getDynamicFormFields, getDynamicFormModels, getExcludeFields
from UserServices.models import Users



# use for  generating dynamic form
class DynamicFormController(APIView):

    # JWT Authentication
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request, modelName):

        # checking our Model is exist in our Dynamic form Models

        if modelName not in getDynamicFormModels():
            return Response ({'error': 'Model not found'}, status=404)
            
        # Getting the model Name from Dynamic Models
        model = getDynamicFormModels() [modelName]
        model_class = apps.get_model(model)
    
        # Getting the model clss from Dynamic odels
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

        # Adding the domain User ID and added by USer ID Post Data'
        fields['domain_user_id'] = request.user.domain_user_id
        fields['added_by_user_id'] = Users.objects.get(id=request.user.id)

        # filtering post data fields by Model Fields and eliminating the extra fields

        fieldsdata={key:value for key, value in fields.items() if key in model_fields}
        print(model_fields)
        print(fields.items())
        print(fieldsdata.items())

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

    def get(self, request, modelName):
        if modelName not in getDynamicFormModels():
            return Response ({'error': 'Model not found'}, status=404)

        model = getDynamicFormModels()[modelName]
        model_class = apps.get_model(model)

        if model_class is None:
            return Response({'error':'model not found'}, status=404)

        model_instance = model_class()
        fields = getDynamicFormFields(model_instance, request.user.domain_user_id)

        return Response({'data':fields, 'message':'Form fields fetched successfully'})
        