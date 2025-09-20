from pydantic import BaseModel, Field

class memory_item(BaseModel):
    key: str = Field(description="The title or name of memory for example: user_name, fav_food, fav_color, age") 
    value: str = Field(description="The actual memory to store")