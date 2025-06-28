from uuid import UUID

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.api.chef_app.repository import DjangoORMChefRepository
from src.api.recipe_app.repository import DjangoORMRecipeRepository
from src.api.recipe_app.serializers import (
    CreateRecipeRequestSerializer,
    CreateRecipeResponseSerializer,
    DeleteRecipeRequestSerializer,
    ListRecipeResponseSerializer,
    RecipeErrorResponseSerializer,
    UpdateRecipeRequestSerializer,
)
from src.core.chef.application.use_cases.exceptions import ChefNotFound
from src.core.recipe.application.use_cases.create_recipe import CreateRecipe
from src.core.recipe.application.use_cases.delete_recipe import DeleteRecipe
from src.core.recipe.application.use_cases.exceptions import InvalidRecipe, RecipeNotFound
from src.core.recipe.application.use_cases.list_recipe_by_chef import ListRecipeByChef
from src.core.recipe.application.use_cases.search_recipe import SearchRecipe
from src.core.recipe.application.use_cases.update_recipe import UpdateRecipe


class RecipeViewSet(viewsets.ViewSet):
    @extend_schema(
        request=CreateRecipeRequestSerializer,
        responses={
            201: CreateRecipeResponseSerializer,
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
                response=RecipeErrorResponseSerializer, description='Validation Entity Error'
            ),
            404: OpenApiResponse(
                response=RecipeErrorResponseSerializer, description='Chef not found Error'
            ),
        },
    )
    def create(self, request: Request) -> Response:
        try:
            serializer = CreateRecipeRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            input = CreateRecipe.Input(**serializer.validated_data)
            use_case = CreateRecipe(
                repository=DjangoORMRecipeRepository(), chef_repository=DjangoORMChefRepository()
            )
            output = use_case.execute(input)

            return Response(
                status=HTTP_201_CREATED,
                data=CreateRecipeResponseSerializer(output).data,
            )
        except InvalidRecipe as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data=RecipeErrorResponseSerializer(dict(detail=str(error))).data,
            )
        except ChefNotFound as error:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data=RecipeErrorResponseSerializer(dict(detail=str(error))).data,
            )

    @extend_schema(
        request=UpdateRecipeRequestSerializer,
        responses={
            204: OpenApiResponse(description='No Content'),
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
                response=RecipeErrorResponseSerializer, description='Validation Entity Error'
            ),
            404: OpenApiResponse(
                response=RecipeErrorResponseSerializer, description='Recipe not found Error'
            ),
        },
    )
    def update(self, request: Request, pk: UUID = None) -> Response:
        try:
            serializer = UpdateRecipeRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            input = UpdateRecipe.Input(**serializer.validated_data, id=pk)
            use_case = UpdateRecipe(repository=DjangoORMRecipeRepository())

            use_case.execute(input)

            return Response(
                status=HTTP_204_NO_CONTENT,
            )
        except InvalidRecipe as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data=RecipeErrorResponseSerializer(dict(detail=str(error))).data,
            )
        except RecipeNotFound as error:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data=RecipeErrorResponseSerializer(dict(detail=str(error))).data,
            )

    @extend_schema(
        responses={
            204: OpenApiResponse(description='No Content'),
            404: OpenApiResponse(
                response=RecipeErrorResponseSerializer, description='Recipe not found Error'
            ),
        },
    )
    def destroy(self, _: Request, pk: UUID = None) -> Response:
        try:
            serializer = DeleteRecipeRequestSerializer(data={'id': pk})
            serializer.is_valid(raise_exception=True)

            input = DeleteRecipe.Input(**serializer.validated_data)
            use_case = DeleteRecipe(repository=DjangoORMRecipeRepository())

            use_case.execute(input)

            return Response(
                status=HTTP_204_NO_CONTENT,
            )
        except RecipeNotFound as error:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data=RecipeErrorResponseSerializer(dict(detail=str(error))).data,
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='chef_name',
                description='Filter by chef name (case insensitive)',
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='ingredient',
                description='Filter recipes containing ingredient (case insensitive)',
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='preparation_method',
                description=(
                    'Filter recipes containing text in preparation method (case insensitive)'
                ),
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='description',
                description='Filter recipes containing text in description (case insensitive)',
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='name',
                description='Filter by recipe name (case insensitive)',
                required=False,
                type=str,
            ),
        ],
        responses={
            200: ListRecipeResponseSerializer,
        },
    )
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request: Request) -> Response:
        name = request.query_params.get('name', None)
        ingredient = request.query_params.get('ingredient', None)
        chef_name = request.query_params.get('chef_name', None)
        description = request.query_params.get('description', None)
        preparation_method = request.query_params.get('preparation_method', None)

        input = SearchRecipe.Input(
            name=name,
            ingredient=ingredient,
            chef_name=chef_name,
            description=description,
            preparation_method=preparation_method,
        )

        use_case = SearchRecipe(repository=DjangoORMRecipeRepository())

        output = use_case.execute(input=input)

        response_serializer = ListRecipeResponseSerializer(output)

        return Response(status=HTTP_200_OK, data=response_serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='chef_id',
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: ListRecipeResponseSerializer,
            404: OpenApiResponse(
                response=RecipeErrorResponseSerializer, description='Chef não encontrado'
            ),
        },
    )
    @action(detail=False, methods=['get'], url_path='chef/(?P<chef_id>[^/.]+)')
    def by_chef(self, _: Request, chef_id: UUID = None) -> Response:
        try:
            chef_repository = DjangoORMChefRepository()
            repository = DjangoORMRecipeRepository()

            input = ListRecipeByChef.Input(chef_id=chef_id)
            use_case = ListRecipeByChef(repository=repository, chef_repository=chef_repository)
            output = use_case.execute(input=input)

            response_serializer = ListRecipeResponseSerializer(output)
            return Response(status=HTTP_200_OK, data=response_serializer.data)

        except ChefNotFound as error:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data=RecipeErrorResponseSerializer(dict(detail=str(error))).data,
            )
