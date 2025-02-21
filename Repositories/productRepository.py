from sqlalchemy import Engine
from sqlalchemy.orm import Session

from Entities import Product

class ProductRepository:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_products(self) -> list[Product]:
        with Session(self.engine) as session:
            return session.query(Product).all()

    def get_product(self, id: int) -> Product:
        with Session(self.engine) as session:
            return session.query(Product).filter(Product.id==id).scalar()

    def update_product(self, product: Product) -> Product:
        with Session(self.engine) as session:
            session.query(Product).filter(Product.id==product.id).update({"name": product.name, "description": product.description})
            return session.query(Product).filter(Product.id==product.id).scalar()

    def create_product(self, product: Product) -> Product:
        with Session(self.engine) as session:
            session.add(product)
            session.commit()
            return session.query(Product).order_by(Product.id.desc()).first()
        
    def delete_product(self, id: int):
        with Session(self.engine) as session:
            session.query(Product).filter(Product.id==id).delete()
            session.commit()