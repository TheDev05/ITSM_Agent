from pydantic import BaseModel, Field

class addition_schema(BaseModel):
    a: int = Field(description = 'first integer')
    b: int = Field(description = 'second integer')