from django.db.models import ForeignKey
from rest_framework.response import Response
from rest_framework.views import exception_handler 
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, MethodNotAllowed
from django.core.exceptions import FieldError
from rest_framework import status

def getDynamicFormModels():
    return {
        'product': 'ProductServices.Products',
        'category': 'ProductServices.Categories',
        'warehouse': 'InventoryServices.warehouse',
    }

def getSuperAdminDynamicFormModels():
    return{
        'modules': 'UserServices.Modules',
    }

def checkisFileField(field):
    return field in ['image', 'file', 'path', 'video', 'audio']

def getExcludeFields():
    return ['id', 'created_at', 'updated_at', 'domain_user_id', 'added_by_user_id', 'created_by_user_id', 'updated_by_user_id']

def getDynamicFormFields(model_instance, domain_user_id):
    fields = {'text':[], 'select':[], 'checkbox':[], 'radio':[], 'textarea':[], 'json':[], 'file':[]}
    for field in model_instance._meta.fields:
        if field.name in getExcludeFields():
            continue
        label = field.name.replace('_', ' ').title()
        fielddata = {
            'name': field.name,

            'label': label,
            'placeholder': 'Enter ' + label,
            'default': model_instance.__dict__[field.name] if field.name in model_instance.__dict__ else '',
            'required': not field.null
        }
        if checkisFileField(field.name):
            fielddata['type'] = 'file'
        elif field.get_internal_type()=='TextField':
            fielddata['type'] = 'textarea'
        elif field.get_internal_type()=='JsonField':
            fielddata['type'] = 'json'
        elif field.get_internal_type() == 'CharField' and field.choices:
            fielddata['type'] = 'select'
            fielddata['options'] = [{'id':'', 'value':choice[1]} for choice in field.choices]

        elif field.get_internal_type() == 'CharField' or field.get_internal_type() == 'IntegerField' or field.get_internal_type() == 'DecimalField' or field.get_internal_type() == 'FloatField':
            fielddata['type'] = 'textarea'
        elif field.get_internal_type() == 'BooleanField' or field.get_internal_type() == 'NullBooleanField': 
            fielddata['type'] = 'checkbox'
        else:
            fielddata['type'] = 'text'
            if isinstance(field,ForeignKey):
                related_model = field.related_model
                related_key = field.name
                related_key_name = ''


                if hasattr(related_model, 'defaultkey'):
                    related_key_name = related_model.defaultkey()
                    options = related_model.objects.filter(domain_user_id=domain_user_id).values_list('id', related_key_name, related_model.defaultkey())
                else:
                    related_key_name = related_model._meta.pk.name
                    options = related_model.objects.filter(domain_user_id=domain_user_id).values_list('id', related_key_name, 'name')

                fielddata['options']=[{'id':option[0],'value':option[1]} for option in options]
                fielddata['type']='select'
        fields[fielddata['type']].append(fielddata)
    return fields

def renderResponse(data, message, status):
    if  status>=200 and status<300:
        return Response({'data':data, 'message':message}, status=status)
    else:
        if isinstance(data, dict):
            return Response({'errors': parseDictToList(data), 'message': message}, status=status)
        elif isinstance(data, list):
            return Response({'errors': data, 'message': message}, status=status)
        else:
            return Response({'errors': [data], 'message': message}, status=status)

def parseDictToList(data):
    # Storing the all value is come in dictionary format
    values = []
    for key, value in data.items():
        values.extend(value)
    # return value which is extract from the data
    return values

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    status_code = getattr(exc, 'status_code', 215)
    if isinstance(exc, AuthenticationFailed):
        response_data ={
            'message': exc.detail,
            'errors': exc.detail.get('messages')
        }
        return renderResponse(data=response_data['errors'], message=response_data['message']['detail'], status=exc.status_code)
    elif isinstance(exc, NotAuthenticated):
        return renderResponse(data="User is not Authenticated", message="User is not Authenticated", status=exc.status_code)
    elif isinstance(exc, PermissionDenied):
        return renderResponse(data="You have not permission to access this page", message='PermissionDenied', status=exc.status_code)
    elif isinstance(exc, MethodNotAllowed):
        return renderResponse(data="On this API This method request is not accepted", message="On this API This method request is not accepted", status=exc.status_code)
    elif isinstance(exc, FieldError):
        return renderResponse(data="There is an field error", message="there is an field error", status=status_code)
    elif isinstance(exc, AttributeError):
        missing_attribute = str(exc)  # Extracts which attribute is missing
        return renderResponse(data={"error": f"AttributeError: {missing_attribute}"}, message="Attribute Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:    
        return renderResponse(data=str(type(exc)), message='Failed', status=exc.status_code)
        # return renderResponse(data=str(type(exc)), message='Failed', status=status_code)
        # return "error"