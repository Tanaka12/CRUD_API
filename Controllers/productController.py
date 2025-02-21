from fastapi import APIRouter, status

from Entities import Product
from Repositories import ProductRepository
from Schemas import ProductSchema
from Services import ContextService

products_router = APIRouter()

@products_router.get("/products", tags=["products"], status_code=status.HTTP_200_OK)
async def get_products():
    return ProductRepository(ContextService.get_item("engine")).get_products()

@products_router.get("/products/{product_id}", tags = ["products"], status_code=status.HTTP_200_OK)
async def get_product(product_id: int):
    return ProductRepository(ContextService.get_item("engine")).get_product(product_id)

@products_router.post("/products", tags = ["products"], status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductSchema):
    product_db = Product(id = product.id, name = product.name, description = product.description)
    return ProductRepository(ContextService.get_item("engine")).create_product(product_db)

@products_router.put("/products", tags = ["products"], status_code=status.HTTP_200_OK)
async def update_product(product: ProductSchema):
    product_db = Product(id = product.id, name = product.name, description = product.description)
    print(product_db)
    return ProductRepository(ContextService.get_item("engine")).update_product(product_db)

@products_router.delete("/products/{product_id}", tags = ["products"], status_code=status.HTTP_200_OK)
async def delete_product(product_id: int):
    ProductRepository(ContextService.get_item("engine")).delete_product(product_id)
    return