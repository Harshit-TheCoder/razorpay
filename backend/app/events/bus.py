from typing import Callable, Dict, List, Any
import asyncio

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event_type: str, payload: Any):
        if event_type in self._subscribers:
            tasks = [
                asyncio.create_task(handler(payload))
                for handler in self._subscribers[event_type]
            ]
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

# Singleton instance
event_bus = EventBus()
