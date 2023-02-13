import time
import uuid

from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sge.data.mongo import database
from sge.domain.helpers import shift_helper
from sge.domain.repositories.crud import (add_data, delete_data, get_data,
                                          get_list_data)
from sge.domain.service import (NoShiftsAvailableException, generate_shift,
                                verify_all_planning_conditions)
from sge.resources.routes.areas import get_employees_by_area
from sge.resources.routes.employees import get_employee_data
from sge.resources.schemas.response import error_schema, response_model
from sge.resources.schemas.shift import ShiftSchema

from sge.domain.shiftservice import ShiftService

router = APIRouter()
collection = database.shifts


# Get a shift
@router.get('/{id}', response_description='Shift data retrieved')
async def get_shift_data(id: uuid.UUID):
    shift = await get_data(collection, shift_helper, str(id))
    if shift:
        return response_model(
            shift, status.HTTP_200_OK, 'Shift data retrieved successfully')
    return error_schema('Shift doesn\'t exist.', status.HTTP_404_NOT_FOUND)

# Create a shift test
@router.post(
    '/test', response_description='Create a new shift',
    status_code=status.HTTP_201_CREATED)
async def create_shift_test(shift: ShiftSchema = Body(...)):
    shift = jsonable_encoder(shift)
    if await get_list_data(
            collection, shift_helper, area=shift['area'],
            year=shift['year'], month=shift['month']):
        return error_schema('Shift already exists.', status.HTTP_409_CONFLICT)
    employees = await get_employees_by_area(
        id=uuid.UUID(shift["area"]), active=True)
    if not isinstance(employees, JSONResponse):
        shift['employees'] = employees['data']
        shift_service = ShiftService()
        shift['shifts'] = await shift_service.generate(shift)#await generate_shift(shift)
        return shift['shifts']
        del shift['employees']
        response = await add_data(
            collection, shift_helper, jsonable_encoder(shift))
        return response_model(
            response, status.HTTP_201_CREATED, 'Shift created successfully.')

    return error_schema('Cannot found employees to create shift.',
                        status.HTTP_404_NOT_FOUND)

# Create a shift
@router.post(
    '/', response_description='Create a new shift',
    status_code=status.HTTP_201_CREATED)
async def create_shift(shift: ShiftSchema = Body(...)):
    shift = jsonable_encoder(shift)
    if await get_list_data(
            collection, shift_helper, area=shift['area'],
            year=shift['year'], month=shift['month']):
        return error_schema('Shift already exists.', status.HTTP_409_CONFLICT)
    employees = await get_employees_by_area(
        id=uuid.UUID(shift["area"]), active=True)
    if not isinstance(employees, JSONResponse):
        shift['employees'] = employees['data']
        shift['shifts'] = await generate_shift(shift)
        del shift['employees']
        response = await add_data(
            collection, shift_helper, jsonable_encoder(shift))
        return response_model(
            response, status.HTTP_201_CREATED, 'Shift created successfully.')

    return error_schema('Cannot found employees to create shift.',
                        status.HTTP_404_NOT_FOUND)


# Create a shift detailed
@router.post(
    '/detail', response_description='Create a new shift detailed',
    status_code=status.HTTP_201_CREATED)
async def create_shift_detail(shift: ShiftSchema = Body(...)):
    shift = shift.dict(exclude_none=True)
    shift = jsonable_encoder(shift)
    if await get_list_data(
            collection, shift_helper, area=shift['area'],
            year=shift['year'], month=shift['month']):
        return error_schema('Shift already exists.', status.HTTP_409_CONFLICT)

    for employee in shift['employees']:
        employee_data = await get_employee_data(uuid.UUID(employee['id']))

        if not isinstance(employee_data, JSONResponse):
            if employee_data['data']['area'] != shift['area']:
                return error_schema(
                    'Area ID doesn\'t match with the employee requested.',
                    status.HTTP_400_BAD_REQUEST)

            employee['name'] = employee_data['data']['name']
        else:
            return error_schema('Employee doesn\'t exist.',
                                status.HTTP_404_NOT_FOUND)

    start_time = time.time()
    seconds = 5
    planning = None
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            break
        planning = await generate_shift(shift)
        if not verify_all_planning_conditions(shift, planning):
            planning = None
            continue
        else:
            break

    if planning is None:
        raise NoShiftsAvailableException(
            'No shifts available by the given parameters.')

    shift['shifts'] = planning
    del shift['employees']
    shift['_id'] = shift.pop('id')
    response = await add_data(
        collection, shift_helper, jsonable_encoder(shift))
    return response_model(
        response, status.HTTP_201_CREATED, 'Shift created successfully.')


# Delete a shift
@router.delete('/{id}', response_description='Shift data deleted')
async def delete_shift_data(id: uuid.UUID):
    response = await delete_data(collection, str(id))
    if response:
        return response_model(
            response, status.HTTP_200_OK, 'Shift deleted successfully')
    return error_schema('Shift doesn\'t exist.', status.HTTP_404_NOT_FOUND)
