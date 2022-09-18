from fastapi import status
from fastapi.responses import JSONResponse

from sge.domain.models.shift import InvalidLeaveDateException
from sge.domain.service import ConflitDateException, NoShiftsAvailableException


def _generate_error(code: int, message: str) -> dict:
    return {
        'content': {
            'error': {
                'code': code,
                'message': message,
            }
        }
    }


def error_handler(app):
    @app.exception_handler(NoShiftsAvailableException)
    def _no_shifts_available_error_handler(request, exc):
        return JSONResponse(
            **_generate_error(
                400,
                'No shifts available by the given parameters.'),
            status_code=status.HTTP_400_BAD_REQUEST)

    @app.exception_handler(ConflitDateException)
    def _conflit_date_error_handler(request, exc):
        return JSONResponse(
            **_generate_error(
                400,
                'Mandatory shift is in a leave period.'),
            status_code=status.HTTP_400_BAD_REQUEST)

    @app.exception_handler(InvalidLeaveDateException)
    def _invalid_leave_date_error_handler(request, exc):
        return JSONResponse(
            **_generate_error(
                400,
                'DateError: leave starts after it ends.'),
            status_code=status.HTTP_400_BAD_REQUEST)
