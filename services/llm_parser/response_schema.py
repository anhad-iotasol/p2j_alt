from langchain.pydantic_v1 import BaseModel, Field

# Class definition for a form and its properties, to be used with the Pydantic parser to get the desired response.
class Property(BaseModel):
    name: str = Field("What is the form property called?")
    type: str = Field(
        "The data type of form propery being entered. E.g. - string,integer,date,etc.")
    default: str = Field(
        "The default value the property takes. Leave blank if not mentioned")


class Form(BaseModel):
    name: str = Field("what is the form called?")
    required: list[str] = Field(
        "List of the names of required properties of the form. Leave it as empty list if none are mentioned.")
    properties: list[Property] = Field("List of the form properties")
