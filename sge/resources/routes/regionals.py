import uuid

from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from sge.data.mongo import database
from sge.domain.helpers import area_helper, regional_helper
from sge.domain.models.regional import Regional, UpdateRegional
from sge.domain.repositories.crud import (add_data, delete_data, get_data,
                                          get_list_data, update_data)
from sge.resources.schemas.response import error_schema, response_model

router = APIRouter()
collection = database.regionals


# Create a new regional
@router.post(
    '/', response_description='Create a new regional',
    status_code=status.HTTP_201_CREATED)
async def create_regional(regional: Regional = Body(...)):
    regional = jsonable_encoder(regional)
    new_regional = await add_data(collection, regional_helper, regional)
    return response_model(
        new_regional, status.HTTP_201_CREATED, 'Regional created successfully')


# Get a list regional
@router.get('/', response_description='Regionals retrieved')
async def get_regionals():
    regionals = await get_list_data(collection, regional_helper)
    if regionals:
        return response_model(
            regionals, status.HTTP_200_OK,
            'Regionals data retrieved successfully')
    return response_model(regionals, status.HTTP_200_OK, 'Empty list returned')


# Get a regional
@router.get('/{id}', response_description='Regional data retrieved')
async def get_regional_data(id: uuid.UUID):
    regional = await get_data(collection, regional_helper, str(id))
    if regional:
        return response_model(
            regional, status.HTTP_200_OK,
            'Regional data retrieved successfully')
    return error_schema('Regional doesn\'t exist.', status.HTTP_404_NOT_FOUND)


# Update a regional
@router.put('/{id}')
async def update_regional_data(id: uuid.UUID, req: UpdateRegional = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_regional = await update_data(collection, str(id), req)
    if updated_regional:
        return response_model(
            f'Regional with ID: {id} name update is successful',
            status.HTTP_200_OK,
            'Regional name updated successfully',
        )
    return error_schema('There was an error updating the regional data.',
                        status.HTTP_400_BAD_REQUEST)


# Delete a regional
@router.delete(
    '/{id}', response_description='Regional data deleted from the database')
async def delete_regional_data(id: uuid.UUID):
    nested_areas = await get_list_data(
        database.areas, area_helper, regional=str(id))
    if nested_areas:
        return error_schema(f'Regional with ID {id} has nested areas.',
                            status.HTTP_400_BAD_REQUEST)
    deleted_regional = await delete_data(collection, str(id))
    if deleted_regional:
        return response_model(
            f'Regional with ID: {id} removed', status.HTTP_200_OK,
            'Regional deleted successfully'
        )
    return error_schema(f'Regional with id {id} doesn\'t exist',
                        status.HTTP_404_NOT_FOUND)
