from fastapi.responses import JSONResponse


def response_model(data: dict, code: int, message: str) -> dict:
    return {
        'data': data,
        'code': code,
        'message': message
    }


def error_model(error: dict, code: int, message: str) -> dict:
    return {
        'error': error,
        'code': code,
        'message': message
    }


def error_schema(message: str, error: int) -> JSONResponse:
    return JSONResponse(
            status_code=error,
            content=error_model(
                'An error occurred.', error, message))
