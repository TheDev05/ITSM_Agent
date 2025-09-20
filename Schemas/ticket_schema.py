from pydantic import BaseModel, Field

class ticket_schema(BaseModel):
    short_description: str =  Field(description = "the summary of user's issue")
    description: str = Field(description = "the explained description of user's issue")