from src.domain.Board import Board
from src.exceptions.Exceptions import ValidationError
from src.repository.BaseRepo import BaseRepo


class BaseService:
    """Base class for all the services."""
    def __init__(self, repository: BaseRepo):
        """
        Initialization of the base class.
        :param repository: The repository the class will use.
        """
        if not isinstance(repository, BaseRepo):
            raise ValidationError("The repository must be of type BaseRepo or inherited from it.")

        self._repo = repository