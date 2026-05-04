import asyncio
from typing import Awaitable, Iterable, TypeVar


T = TypeVar("T")


async def gather_tasks(tasks: Iterable[Awaitable[T]]) -> list[T]:
    return list(await asyncio.gather(*tasks))
