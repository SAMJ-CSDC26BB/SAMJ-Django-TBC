import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from ..businessLogic import getDestination


class DestinationSerializer(serializers.Serializer):
    destination = serializers.CharField()


class api_v2_tbc(APIView):
    @swagger_auto_schema(
        operation_summary="Called +E164",
        manual_parameters=[
            openapi.Parameter(
                'number',
                openapi.IN_QUERY,
                description="get dest. number if current Time matches callforwarding Entry corresponding to "
                            "called number",
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
