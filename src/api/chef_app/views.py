from drf_spectacular.utils import OpenApiExample, OpenApiResponse, OpenApiTypes, extend_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.api.chef_app.repository import DjangoORMChefRepository
from src.api.chef_app.serializers import (
    ChefErrorResponseSerializer,
    CreateChefRequestSerializer,
    CreateChefResponseSerializer,
)
from src.core.chef.application.use_cases.create_chef import CreateChef
from src.core.chef.application.use_cases.exceptions import InvalidChef


class ChefViewSet(viewsets.ViewSet):
    @extend_schema(
        request=CreateChefRequestSerializer,
        responses={
            201: CreateChefResponseSerializer,
            400: OpenApiResponse(
                description='Validation Error',
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Error example',
                        value={
                            'name': ['This field may not be blank.'],
                        },
                    )
                ],
            ),
            422: OpenApiResponse(
                response=ChefErrorResponseSerializer, description='Validation Entity Error'
            ),
        },
    )
    def create(self, request: Request) -> Response:
        try:
            serializer = CreateChefRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            input = CreateChef.Input(**serializer.validated_data)
            use_case = CreateChef(repository=DjangoORMChefRepository())
            output = use_case.execute(input)

            return Response(
                status=HTTP_201_CREATED,
                data=CreateChefResponseSerializer(output).data,
            )
        except InvalidChef as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data=ChefErrorResponseSerializer(dict(detail=str(error))).data,
            )
