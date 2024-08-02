from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pymongo.errors import PyMongoError

from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.pantry import (
    Categories,
    CategoryValue,
    Items,
    Pantry,
    pantry_example,
)
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


async def create_category(current_user_pantry, category_value):
    if str(category_value.value) not in current_user_pantry.pantry:
        current_user_pantry.pantry[category_value.value] = Categories(
            category_value=category_value, category_name=category_value.name
        )

        await current_user_pantry.save()


async def add_item_to_list(current_user_pantry, category_value, item):
    item_list = current_user_pantry.pantry[str(category_value.value)]['items']

    item_exist = any(
        dict_item_list['item_name'] == item.item_name for dict_item_list in item_list
    )

    if item_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Já existe um item com o mesmo nome {item.item_name}.',
        )

    current_user_pantry.pantry[str(category_value.value)]['items'].append(
        item.model_dump()
    )

    await current_user_pantry.save()


async def get_pantry_collection(current_user_id: PydanticObjectId):
    try:
        pantry_collection = await Pantry.find(
            Pantry.user_id == current_user_id,
        ).first_or_none()
        return pantry_collection
    except PyMongoError as e:
        # TODO: Log ou exiba uma mensagem de erro apropriada
        print(f'Erro ao consultar o banco de dados: {e}')
        # Ou lançar uma exceção personalizada se necessário
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Erro ao acessar o banco de dados.',
        )


@router.post('/{user_id}/item/{category}', status_code=status.HTTP_201_CREATED)
async def create_item_pantry(
    user_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item: Items = Body(example=pantry_example),
):
    """
    **Lista dos valores de cada categoria de alimento**\n
    Pães e Produtos de Panificação = 101,\n
    Doces = 102,\n
    Produtos Enlatados e Conservas = 103,\n
    Materiais de Limpeza = 104,\n
    Condimentos e Molhos = 105,\n
    Laticínios e Ovos = 106,\n
    Bebidas = 107,\n
    Congelados = 108,\n
    Frutas e Vegetais = 109,\n
    Grãos e Cereais = 110,\n
    Produtos de Mercearia = 111,\n
    Lavanderia = 112,\n
    Carne e Peixe = 113,\n
    Massas e Produtos de Trigo = 114,\n
    Higiene Pessoal = 115,\n
    Temperos e Ervas Secas = 116,\n
    Papelaria = 117\n
    """

    check_user_permission(current_user.id, user_id)  # type: ignore

    pantry_collection = await get_pantry_collection(current_user.id)  # type: ignore

    if not pantry_collection:
        # Cria o um Document Pantry na collection pantry.
        current_user_pantry = await Pantry(user_id=current_user.id).insert()

        await create_category(current_user_pantry, category_value)

        await add_item_to_list(current_user_pantry, category_value, item)

    else:
        await create_category(pantry_collection, category_value)

        await add_item_to_list(pantry_collection, category_value, item)

    return {'detail': f'Item {item.item_name} adicionado'}
