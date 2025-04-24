from pydantic import BaseModel, Field

class RegisterSchema(BaseModel):
    full_name: str = Field(
      max_length=64,
      min_length=3,
      description="Full name"
    )
    email: str = Field(
      max_length=100,
      min_length=5,
      pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
      description="Email",
      examples=["example@email.com"]
    )
    password: str = Field(min_length=8, description="Password")

class LoginSchema(BaseModel):
    email: str = Field(
      max_length=100,
      min_length=5,
      pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
      description="Email",
      examples=["example@email.com"]
    )
    password: str = Field(min_length=8, description="Password")
