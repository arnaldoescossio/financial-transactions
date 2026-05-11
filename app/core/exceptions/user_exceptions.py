from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self, identifier: str = ""):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found{f': {identifier}' if identifier else ''}.",
        )


class UserAlreadyExistsException(HTTPException):
    def __init__(self, identifier: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with {identifier} already exists.",
        )


class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )


class InsufficientPermissionsException(HTTPException):
    def __init__(self, required_role: str = ""):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions{f'. Required role: {required_role}' if required_role else ''}.",
        )


class PasswordValidationException(HTTPException):
    def __init__(self, detail: str = "Password does not meet requirements."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=detail,
        )
