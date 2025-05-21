from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: str
    size: float
    unit: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True