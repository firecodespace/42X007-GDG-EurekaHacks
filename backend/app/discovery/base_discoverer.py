from abc import ABC, abstractmethod
from typing import Iterable
from app.discovery.discovered_url import DiscoveredURL


class BaseDiscoverer(ABC):
    """
    A discoverer ONLY finds URLs.
    It does not fetch HTML.
    It does not parse content.
    """

    @abstractmethod
    def discover(self) -> Iterable[DiscoveredURL]:
        pass
