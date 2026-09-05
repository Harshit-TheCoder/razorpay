from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any

T = TypeVar("T")

class AbstractRepository(ABC, Generic[T]):
    
    @abstractmethod
    async def get(self, id: Any) -> Optional[T]:
        pass

    @abstractmethod
    async def list(self, limit: int = 20, cursor: Optional[str] = None, **kwargs) -> List[T]:
        pass

    @abstractmethod
    async def create(self, obj: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: Any, obj: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: Any) -> bool:
        pass
