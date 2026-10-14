class AppError(Exception):
    """Base class for all custom app exceptions."""
    pass

class ValidationError(AppError):
    """Raised when input data is invalid."""
    pass

class GameNotFinishedError(AppError):
    """Raised when an action that is not permitted during a game is made."""
    pass