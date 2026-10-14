import pytest

from src.domain.Board import Board
from src.exceptions.Exceptions import ValidationError
from src.repository.MemoryRepo import MemoryRepo
from src.services.BaseService import BaseService


class TestBaseService:
    @pytest.fixture
    def service(self):
        repo = MemoryRepo(Board())
        return BaseService(repo)

    def test_initialization(self):
        with pytest.raises(ValidationError):
            BaseService("ahaga")

        repo = MemoryRepo(Board())
        service = BaseService(repo)
        assert service._repo is repo

