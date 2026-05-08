from abc import ABC, abstractmethod
from typing import Any


class IChallengeService(ABC):
    @abstractmethod
    def get_challenges(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def create_challenge(self, title: str) -> dict[str, str]:
        pass
