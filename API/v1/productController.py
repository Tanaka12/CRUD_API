from fastapi import APIRouter, status, HTTPException
import os

from Entities import Product
from Repositories import ProductRepository
from Schemas import ProductSchema
from Services import ContextService, ImageService

def product_entity_to_schema(product_entity: Product) -> ProductSchema:
    return ProductSchema(id = product_entity.id,
                         name = product_entity.name,
                         description = product_entity.description,
                         image = ImageService().load_image(product_entity.image_path))

def product_schema_to_entity(product_schema: ProductSchema, image_path: str) -> Product:
    return Product(id = product_schema.id,
                   name = product_schema.name,
                   description = product_schema.description,
                   image_path = image_path)

def generate_image_path() -> str:
    return "Images/" + os.urandom(32).hex()

router = APIRouter()

@router.get("/products", tags=["products"], status_code=status.HTTP_200_OK, response_model=list[ProductSchema])
async def get_products():
    return map(lambda product: product_entity_to_schema(product), ProductRepository(ContextService.get_item("engine")).get_products())

@router.get("/products/{product_id}", tags = ["products"], status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def get_product(product_id: int):
    product = ProductRepository(ContextService.get_item("engine")).get_product(product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

    return product_entity_to_schema(product)

@router.post("/products", tags = ["products"], status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
async def create_product(product: ProductSchema):
    image_path = generate_image_path()
    ImageService().save_image(product.image, image_path)
    
    product_entity = ProductRepository(ContextService.get_item("engine")).create_product(product_schema_to_entity(product, image_path))
    
    return product_entity_to_schema(product_entity)

@router.put("/products", tags = ["products"], status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def update_product(product: ProductSchema):
    product_entity = ProductRepository(ContextService.get_item("engine")).get_product(product.id)
    if product_entity is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    
    ImageService().save_image(product.image, product_entity.image_path)
    updated_product_entity = ProductRepository(ContextService.get_item("engine")).update_product(product_schema_to_entity(product, product_entity.image_path))

    return product_entity_to_schema(updated_product_entity)

@router.delete("/products/{product_id}", tags = ["products"], status_code=status.HTTP_200_OK)
async def delete_product(product_id: int):
    product_entity = ProductRepository(ContextService.get_item("engine")).get_product(product_id)
    if product_entity is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    
    ProductRepository(ContextService.get_item("engine")).delete_product(product_id)
    return