from pydantic import BaseModel, Field , EmailStr 


class TaskAddSchema(BaseModel):
    title: str = Field(max_length=50)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    


class TaskSchema(TaskAddSchema):
    id: int



class UserCreateSchema(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=8,max_length=50)


class UserResponseSchema(BaseModel):
    id: int
    username: str = Field(max_length=50)
    email: EmailStr


class UserLoginSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(min_length=8,max_length=50)