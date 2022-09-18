from fastapi import FastAPI

from sge.errors import error_handler
from sge.resources.routes.areas import router as areas_router
from sge.resources.routes.employees import router as employees_router
from sge.resources.routes.regionals import router as regionals_router
from sge.resources.routes.shifts import router as shifts_router

app = FastAPI()

error_handler(app)

app.include_router(
    regionals_router, prefix='/api/v1/regionals', tags=['Regionals'])
app.include_router(
    areas_router, prefix='/api/v1/areas', tags=['Areas'])
app.include_router(
    employees_router, prefix='/api/v1/employees', tags=['Employees'])
app.include_router(
    shifts_router, prefix='/api/v1/shifts', tags=['Shifts'])

@app.get('/')
def _():
    return {"message": "Hello World"}
