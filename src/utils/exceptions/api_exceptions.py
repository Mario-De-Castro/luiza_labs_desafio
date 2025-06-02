from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.utils.helpers.helpers_functions import HelperFunctions

from .exceptions import (
    SchemaValidationError,
    GenericExceptions,
    UnauthorizedException
)

logger = HelperFunctions.get_logger()

async def data_already_exists_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=409,
        content={"message": exc.detail},
    )

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=401,
        content={"message": "Unauthorized access. Please provide valid credentials."},
    )

async def no_result_found_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=404,
        content={"message": "No records found for the given parameters."},
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"message": "Database integrity error."},
    )

async def schema_validate_handler(request: Request, exc: SchemaValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": exc._message},
    )

async def generic_exception_handler(request: Request, exc: GenericExceptions):
    logger.error(exc._message)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error has occurred. Please try again later."},
    )
