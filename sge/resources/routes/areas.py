import uuid

from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sge.data.mongo import database
from sge.domain.helpers import area_helper, employee_helper, shift_helper
from sge.domain.models.area import Area, UpdateArea
from sge.domain.repositories.crud import (add_data, delete_data, get_data,
                                          get_list_data, update_data)
from sge.resources.routes.regionals import get_regional_data
from sge.resources.schemas.response import error_schema, response_model

router = APIRouter()
collection = database.areas


# Create a new area
@router.post(
    '/', response_description='Create a new area',
    status_code=status.HTTP_201_CREATED)
async def create_area(area: Area = Body(...)):
    area = jsonable_encoder(area)
    regional = await get_regional_data(uuid.UUID(area["regional"]))
    if not isinstance(regional, JSONResponse):
        new_area = await add_data(collection, area_helper, area)
        return response_model(
            new_area, status.HTTP_201_CREATED, 'Area created successfully')
    return error_schema('Regional doesn\'t exist', status.HTTP_404_NOT_FOUND)


# Get a list area
@router.get('/', response_description='Areas retrieved')
async def get_areas():
    areas = await get_list_data(collection, area_helper)
    if areas:
        return response_model(
            areas, status.HTTP_200_OK,
            'Areas data retrieved successfully')
    return response_model(
        areas, status.HTTP_200_OK, 'Empty list returned')


# Get a area
@router.get('/{id}', response_description='Area data retrieved')
async def get_area_data(id: uuid.UUID):
    area = await get_data(collection, area_helper, str(id))
    if area:
        return response_model(
            area, status.HTTP_200_OK, 'Area data retrieved successfully')
    return error_schema('Area doesn\'t exist', status.HTTP_404_NOT_FOUND)


# Update a area
@router.put('/{id}')
async def update_area_data(id: uuid.UUID, req: UpdateArea = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_area = await update_data(collection, str(id), req)
    if updated_area:
        return response_model(
            f'Area with ID: {id} name update is successful',
            status.HTTP_200_OK,
            'Area name updated successfully',
        )
    return error_schema('There was an error updating the area data.',
                        status.HTTP_400_BAD_REQUEST)


# Delete a area
@router.delete(
    '/{id}',
    response_description='Area data deleted from the database')
async def delete_area_data(id: uuid.UUID):
    nested_employees = await get_list_data(
        database.employees, employee_helper, area=str(id))
    if nested_employees:
        return error_schema(f'Area with ID {id} has nested employees',
                            status.HTTP_400_BAD_REQUEST)
    deleted_area = await delete_data(collection, str(id))
    if deleted_area:
        return response_model(
            'Area with ID: {} removed'.format(id),
            204, 'Area deleted successfully'
        )
    return error_schema(f'Area with id {id} doesn\'t exist',
                        status.HTTP_404_NOT_FOUND)


# Get a list employee by area
@router.get('/{id}/employees', response_description='Employees retrieved')
async def get_employees_by_area(id: uuid.UUID, active: bool):
    employees = await get_list_data(
        database.employees, employee_helper, area=str(id), active=active)
    if employees:
        return response_model(
            employees, status.HTTP_200_OK,
            'Employees data retrieved successfully')
    return error_schema('Employees doesn\'t exist.', status.HTTP_404_NOT_FOUND)


# Get a List with all shifts by area
@router.get('/{id}/shifts', response_description='List all shifts by area')
async def get_shifts_by_area(area: uuid.UUID):
    shifts = await get_list_data(database.shifts, shift_helper, area=str(area))
    if shifts:
        return response_model(
            shifts, status.HTTP_200_OK, 'Shifts data retrieved successfully')
    return response_model(shifts, status.HTTP_200_OK, 'Empty list returned')
