from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import models, schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/products/",
    response_model=schemas.Product,
    summary="Create a product",
    description="""
Create a new product with name, category (like 'fridge' or 'storage'), size y unit.

""",
    tags=["Products"]
)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        name=product.name,
        category=product.category,
        size=product.size,
        unit=product.unit
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get(
    "/products/",
    response_model=List[schemas.Product],
    summary="List products",
    description="Returns a list with all products in database.",
    tags=["Products"]
)
def read_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.get(
    "/products/{category}",
    response_model=List[schemas.Product],
    summary="List products from category",
    description="Returns a list with all products from a specific category.",
    tags=["Products"]
)
def read_products_category(category: str, db: Session = Depends(get_db)):
    return db.query(models.Product).filter(models.Product.category == category).all()

@app.put(
    "/products/{product_id}",
    response_model=schemas.Product,
    summary="Update products",
    description="Updates data from specific product",
    tags=["Products"]
)
def update_product(product_id: int, updated_product: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_product.name
    product.category = updated_product.category
    product.size = updated_product.size
    product.unit = updated_product.unit

    db.commit()
    db.refresh(product)
    return product

@app.delete(
    "/products/{product_id}",
    status_code = 204,
    summary="Delete products",
    description="Deletes a specific product",
    tags=["Products"]
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return None