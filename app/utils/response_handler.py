from flask import jsonify
from typing import Any, Dict, Optional, Union

def api_response(
    success: bool = True,
    message: str = "",
    data: Optional[Any] = None,
    errors: Optional[Union[str, Dict, list]] = None,
    status_code: int = 200
) -> tuple:
    """
    Create a standardized API response
    
    Args:
        success (bool): Indicates if the request was successful
        message (str): Message to be sent in response
        data (Any): Data to be sent in response
        errors (Union[str, Dict, list]): Error details
        status_code (int): HTTP status code
    
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {
        "success": success,
        "message": message,
        "data": data
    }

    if errors is not None:
        response["errors"] = errors

    return jsonify(response), status_code


def success_response(
    data: Optional[Any] = None,
    message: str = "Success",
    status_code: int = 200
) -> tuple:
    """
    Create a success response
    """
    return api_response(
        success=True,
        message=message,
        data=data,
        status_code=status_code
    )


def error_response(
    message: str = "Error occurred",
    errors: Optional[Union[str, Dict, list]] = None,
    status_code: int = 400
) -> tuple:
    """
    Create an error response
    """
    return api_response(
        success=False,
        message=message,
        errors=errors,
        status_code=status_code
    ) 