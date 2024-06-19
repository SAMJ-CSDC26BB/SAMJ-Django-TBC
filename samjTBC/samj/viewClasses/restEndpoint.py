from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..businessLogic import getDestination
import logging

class DestinationSerializer(serializers.Serializer):
    destination = serializers.CharField()

class restEndpoint(APIView):
    @swagger_auto_schema(
        operation_summary="Get destination based on query",
        manual_parameters=[
            openapi.Parameter(
                'number',
                openapi.IN_QUERY,
                description="Number parameter for querying destination",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: DestinationSerializer,
            400: "Bad Request: Invalid input",
        },
    )
    def get(self, request):
        logger = logging.getLogger("samj")
        query = request.GET.get('number', '')
        logger.info("query -> " + query)

        # Call your business logic function
        dest = getDestination(query)
        logger.info("dest -> " + dest)

        # Serialize the response data
        serializer = DestinationSerializer({'destination': dest})

        return Response(serializer.data)
