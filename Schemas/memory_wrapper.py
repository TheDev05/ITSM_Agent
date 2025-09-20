from pydantic import BaseModel, Field
from Schemas.memory_item import memory_item

class memory_wrapper(BaseModel):
    memory: list[memory_item] = Field(description="List of memory items")