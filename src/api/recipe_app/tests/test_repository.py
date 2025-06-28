from uuid import uuid4

import pytest

from src.api.chef_app.repository import DjangoORMChefRepository
from src.api.recipe_app.models import RecipeModel
from src.api.recipe_app.repository import DjangoORMRecipeRepository
from src.core.chef.domain.chef import Chef
from src.core.recipe.domain.recipe import Recipe
from src.core.recipe.domain.recipe_repository import SearchFilterRecipe


@pytest.mark.django_db
def test_saves_recipe_in_database():
    chef = Chef(
        name='Test Chef',
    )
    chef_repository = DjangoORMChefRepository()
    chef_repository.save(chef)

    recipe = Recipe(
        chef_id=chef.id,
        name='Brigadeiro',
        description='Receita de Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
    )

    recipe_repository = DjangoORMRecipeRepository()

    assert RecipeModel.objects.count() == 0
    recipe_repository.save(recipe=recipe)
    assert RecipeModel.objects.count() == 1
    saved_recipe = RecipeModel.objects.get()

    assert saved_recipe.id == recipe.id
    assert saved_recipe.chef.id == recipe.chef_id
    assert saved_recipe.name == recipe.name
    assert saved_recipe.description == recipe.description
    assert saved_recipe.ingredients == recipe.ingredients
    assert saved_recipe.preparation_method == recipe.preparation_method
    assert saved_recipe.is_active == recipe.is_active


@pytest.mark.django_db
def test_update_recipe_in_database():
    chef = Chef(
        name='Test Chef',
    )
    chef_repository = DjangoORMChefRepository()
    chef_repository.save(chef)

    recipe = Recipe(
        chef_id=chef.id,
        name='Brigadeiro',
        description='Receita de Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
    )

    recipe_repository = DjangoORMRecipeRepository()
    recipe_repository.save(recipe=recipe)

    recipe.update(
        name='Updated name',
        description='Updated Description',
        ingredients=['Updated Ingredients'],
        preparation_method='Updated preparation',
    )

    recipe_repository.update(recipe)

    updated_recipe = recipe_repository.get_by_id(id=recipe.id)

    assert updated_recipe.name == 'Updated name'
    assert updated_recipe.description == 'Updated Description'
    assert updated_recipe.ingredients == ['Updated Ingredients']
    assert updated_recipe.preparation_method == 'Updated preparation'


@pytest.mark.django_db
def test_delete_recipe_in_database():
    chef = Chef(
        name='Test Chef',
    )
    chef_repository = DjangoORMChefRepository()
    chef_repository.save(chef)

    recipe = Recipe(
        chef_id=chef.id,
        name='Brigadeiro',
        description='Receita de Brigadeiro',
        ingredients=[
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        preparation_method='Misture tudo e leve al fogo médio até pegar o ponto',
    )

    recipe_repository = DjangoORMRecipeRepository()
    recipe_repository.save(recipe=recipe)

    assert RecipeModel.objects.count() == 1

    recipe_repository.delete(recipe.id)

    assert RecipeModel.objects.count() == 0

    deleted_recipe = recipe_repository.get_by_id(id=recipe.id)

    assert deleted_recipe is None


@pytest.mark.django_db
def test_search():
    chef = Chef(
        name='Test Chef',
    )
    chef_repository = DjangoORMChefRepository()
    chef_repository.save(chef)

    recipe_repository = DjangoORMRecipeRepository()
    recipe_repository.save(
        recipe=Recipe(
            chef_id=chef.id,
            name='Brigadeiro',
            description='Receita de Brigadeiro',
            ingredients=[
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            preparation_method=(
                'Coloque os ovos em um frigideira no fogo baixo e mexa, depois de'
                ' pontro jogue o requeijão.'
            ),
        )
    )

    recipe_repository.save(
        recipe=Recipe(
            chef_id=chef.id,
            name='Ovo mexido',
            description='Receita de ovo mexido',
            ingredients=[
                '2 Ovos',
                '1/2 Colher de Sopa de Mateiga',
                '1 Colher de sopa de requeijão',
            ],
            preparation_method='Misture tudo e leve ao fogo médio até pegar o ponto',
        )
    )

    assert RecipeModel.objects.count() == 2

    recipes = recipe_repository.search(SearchFilterRecipe(name='brigadeiro'))

    assert len(recipes) == 1
    assert recipes[0].name == 'Brigadeiro'

    recipes = recipe_repository.search(SearchFilterRecipe(ingredient='ovo'))

    assert len(recipes) == 1
    assert recipes[0].name == 'Ovo mexido'

    recipes = recipe_repository.search(SearchFilterRecipe(chef_name='test Chef'))

    assert len(recipes) == 2
    assert recipes[0].name == 'Brigadeiro'
    assert recipes[1].name == 'Ovo mexido'

    recipes = recipe_repository.search(SearchFilterRecipe(preparation_method='fogo'))

    assert len(recipes) == 2
    assert recipes[0].name == 'Brigadeiro'
    assert recipes[1].name == 'Ovo mexido'

    recipes = recipe_repository.search(SearchFilterRecipe(description='receita'))

    assert len(recipes) == 2
    assert recipes[0].name == 'Brigadeiro'
    assert recipes[1].name == 'Ovo mexido'


@pytest.mark.django_db
def test_list_by_chef_id():
    chef = Chef(
        name='Test Chef',
    )
    chef_repository = DjangoORMChefRepository()
    chef_repository.save(chef)

    recipe_repository = DjangoORMRecipeRepository()
    recipe_repository.save(
        recipe=Recipe(
            chef_id=chef.id,
            name='Brigadeiro',
            description='Receita de Brigadeiro',
            ingredients=[
                '1 Lata de Leite Condensado',
                '2 Colheres de Sopa de Achocolatado',
                '1 Colher de Chá de Manteiga',
            ],
            preparation_method=(
                'Coloque os ovos em um frigideira no fogo baixo e mexa, depois de'
                ' pontro jogue o requeijão.'
            ),
        )
    )

    recipe_repository.save(
        recipe=Recipe(
            chef_id=chef.id,
            name='Ovo mexido',
            description='Receita de ovo mexido',
            ingredients=[
                '2 Ovos',
                '1/2 Colher de Sopa de Mateiga',
                '1 Colher de sopa de requeijão',
            ],
            preparation_method='Misture tudo e leve ao fogo médio até pegar o ponto',
        )
    )

    assert RecipeModel.objects.count() == 2

    recipes = recipe_repository.list_by_chef_id(chef_id=chef.id)

    assert len(recipes) == 2

    recipes = recipe_repository.list_by_chef_id(chef_id=uuid4())

    assert len(recipes) == 0
