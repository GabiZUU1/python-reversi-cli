import pytest

from src.domain.Board import Board
from src.repository.MemoryRepo import MemoryRepo


class TestMemoryRepo:
    def test_initialization(self):
        b = Board()
        repo = MemoryRepo(b)

        assert repo.board is b
        assert repo.player1 is None
        assert repo.player2 is None