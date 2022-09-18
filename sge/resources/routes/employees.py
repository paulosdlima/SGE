import uuid

from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sge.data.mongo import database
from sge.domain.helpers import employee_helper
from sge.domain.models.employee import Employee, UpdateEmployee
from sge.domain.repositories.crud import (add_data, delete_data, get_data,
                                          get_list_data, update_data)
from sge.resources.routes.areas import get_area_data
from sge.resources.schemas.response import error_schema, response_model

router = APIRouter()
collection = database.employees


# Create a new employee
@router.post(
    '/', response_description='Create a new employee',
    status_code=status.HTTP_201_CREATED)
async def create_employee(employee: Employee = Body(...)):
    employee = jsonable_encoder(employee)
    area = await get_area_data(uuid.UUID(employee['area']))
    if not isinstance(area, JSONResponse):
        new_employee = await add_data(collection, employee_helper, employee)
        return response_model(
            new_employee, status.HTTP_201_CREATED,
            'Employee created successfully')
    return error_schema('Area doesn\'t exist.', status.HTTP_404_NOT_FOUND)


# Get a list employee
@router.get('/', response_description='Employees retrieved')
async def get_employees():
    employees = await get_list_data(collection, employee_helper)
    if employees:
        return response_model(
            employees, status.HTTP_200_OK,
            'Employees data retrieved successfully')
    return response_model(employees, status.HTTP_200_OK, 'Empty list returned')


# Get a employee
@router.get('/{id}', response_description='Employee data retrieved')
async def get_employee_data(id: uuid.UUID):
    employee = await get_data(collection, employee_helper, str(id))
    if employee:
        return response_model(
            employee, status.HTTP_200_OK,
            'Employee data retrieved successfully')
    return error_schema('Employee doesn\'t exist.', status.HTTP_404_NOT_FOUND)


# Update a employee
@router.put('/{id}')
async def update_employee_data(id: uuid.UUID, req: UpdateEmployee = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_employee = await update_data(collection, str(id), req)
    if updated_employee:
        return response_model(
            f'Employee with ID: {id} name update is successful',
            status.HTTP_200_OK, 'Employee name updated successfully',
        )
    return error_schema('There was an error updating the employee data.',
                        status.HTTP_400_BAD_REQUEST)


@router.put('/{id}/transfer/{area}')
async def transfer_employee(id: uuid.UUID, area: uuid.UUID):
    if isinstance(await get_employee_data(id), JSONResponse):
        return error_schema('Employee doesn\'t exist.',
                            status.HTTP_404_NOT_FOUND)
    data = await get_area_data(area)
    if not isinstance(data, JSONResponse):
        updated_employee = await update_data(
            collection, str(id), {'area': str(area)})
        if updated_employee:
            return response_model(
                f'Employee with ID {id} was transfered successfully',
                status.HTTP_200_OK, 'Employee transfered successfully',
            )
        return error_schema('There was an error updating the employee data.',
                            status.HTTP_400_BAD_REQUEST)
    return error_schema('Area doesn\'t exist.', status.HTTP_404_NOT_FOUND)


# Delete a employee
@router.delete(
    '/{id}',
    response_description='Employee data deleted from the database')
async def delete_employee_data(id: uuid.UUID):
    deleted_employee = await delete_data(collection, str(id))
    if deleted_employee:
        return response_model(
            f'Employee with ID: {id} removed', status.HTTP_200_OK,
            'Employee deleted successfully'
        )
    return error_schema(f'Employee with id {id} doesn\'t exist',
                        status.HTTP_404_NOT_FOUND)
