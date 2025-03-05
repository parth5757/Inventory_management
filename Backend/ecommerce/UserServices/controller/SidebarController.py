import json
from UserServices.models import Modules
from django.core.serializers import serialize
from rest_framework import generics, status
from rest_framework.response import Response

class ModuleView(generics.CreateAPIView):
    def get(self, request):
        # Order by a valid field from Modules model
        menus = Modules.objects.filter(is_menu=True).order_by('display_order')
        
        # Serialize the queryset to JSON string
        serialized_menu = serialize('json', menus)
        
        # Convert JSON string to Python data (list/dict)
        menu_data = json.loads(serialized_menu)
        
        # Log or print if needed (use print properly)
        # print("Data:", menu_data, "Message:", "All Modules", "Status:", status.HTTP_200_OK)
        

        return Response(data=menu_data, status=status.HTTP_200_OK, 
                        headers={"Message": "All Modules"})
