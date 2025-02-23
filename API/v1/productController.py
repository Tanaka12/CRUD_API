from fastapi import APIRouter, status, HTTPException

from Entities import Product
from Repositories import ProductRepository
from Schemas import ProductSchema
from Services import ContextService

router = APIRouter()

@router.get("/products", tags=["products"], status_code=status.HTTP_200_OK)
async def get_products():
    return ProductRepository(ContextService.get_item("engine")).get_products()

@router.get("/products/{product_id}", tags = ["products"], status_code=status.HTTP_200_OK)
async def get_product(product_id: int):
    product = ProductRepository(ContextService.get_item("engine")).get_product(product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

    return ProductSchema(id = product.id, name = product.name, description = product.description)

@router.post("/products", tags = ["products"], status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductSchema):
    product_entity = Product(name = product.name, description = product.description)
    return ProductRepository(ContextService.get_item("engine")).create_product(product_entity)

@router.put("/products", tags = ["products"], status_code=status.HTTP_200_OK)
async def update_product(product: ProductSchema):
    product_entity = Product(id = product.id, name = product.name, description = product.description)
    if ProductRepository(ContextService.get_item("engine")).update_product(product_entity) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    
    return product_entity

@router.delete("/products/{product_id}", tags = ["products"], status_code=status.HTTP_200_OK)
async def delete_product(product_id: int):
    ProductRepository(ContextService.get_item("engine")).delete_product(product_id)
    return