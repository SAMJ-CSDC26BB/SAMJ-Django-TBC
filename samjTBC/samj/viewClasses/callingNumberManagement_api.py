import json
import logging
from django.http import JsonResponse
from django.views import View

from ..models import DestinationNumber, GlobalSettings, User
from ..views import validate_password

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.mixins import LoginRequiredMixin



@method_decorator(csrf_exempt, name='dispatch')
class callingNumberManagementAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        destinations = DestinationNumber.objects.all().values('number', 'name')
        destinations_list = list(destinations)
        destinations_list_wrapped = {'destinations' : destinations_list}
        logger = logging.getLogger("samj")
        logger.info(destinations_list_wrapped)
        return JsonResponse(destinations_list_wrapped)

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger("samj")
        logger.info("post request triggered")

        try:
            data = json.loads(request.body)
            destination = DestinationNumber(
                name=data.get('name'),
                number=data.get('number'),
            )
            destination.save()
            return JsonResponse({'message': 'Destination created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        logger = logging.getLogger("samj")
        logger.info("put request triggered")

        try:
            data = json.loads(request.body)
            destination_number = data.get('number')
            destination_name = data.get('name')
            if not destination_number:
                return JsonResponse({'error': 'Number is required for updating a destination'}, status=400)
            try:
                destination = DestinationNumber.objects.get(number=destination_number, name=destination_name)
            except DestinationNumber.DoesNotExist:
                return JsonResponse({'error': 'Destination not found'}, status=404)

            destination.name = data.get('name', destination.name)
            destination.number = data.get('number', destination.number)
            destination.save()
            return JsonResponse({'message': 'Destination updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        logger = logging.getLogger("samj")
        logger.info("delete request triggered")

        try:
            user = request.user
            data = json.loads(request.body)
            destination_id = data.get('id')
            if not destination_id:
                return JsonResponse({'error': 'ID is required for deleting a destination'}, status=400)
            try:
                destination = DestinationNumber.objects.get(id=destination_id, user=user)
            except DestinationNumber.DoesNotExist:
                return JsonResponse({'error': 'Destination not found'}, status=404)

            destination.delete()
            return JsonResponse({'message': 'Destination deleted successfully'}, status=204)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)