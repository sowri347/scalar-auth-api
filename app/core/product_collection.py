from typing import List, Dict, Any
from app.core.database import get_database

PRODUCT_COLLECTION = "products"

async def get_product_collection():
    db = get_database()
    return db[PRODUCT_COLLECTION]

async def seed_products():
    """Insert sample products if not already present"""
    product_collection = await get_product_collection()
    count = await product_collection.count_documents({})
    if count == 0:
        products = [
            {"product_id": "P001", "name": "iPhone 15 Pro", "price": 139999, "category": "Smartphone", "image": "/images/iphone15pro.jpg"},
            {"product_id": "P002", "name": "MacBook Air M3", "price": 124999, "category": "Laptop", "image": "/images/macbook.jpg"},
            {"product_id": "P003", "name": "Sony WH-1000XM5", "price": 29999, "category": "Headphones", "image": "/images/sonyheadphones.jpg"},
            {"product_id": "P004", "name": "Apple Watch Ultra 2", "price": 89999, "category": "Smartwatch", "image": "/images/watchultra.jpg"},
            {"product_id": "P005", "name": "iPad Pro M4", "price": 119999, "category": "Tablet", "image": "/images/ipadpro.jpg"},
            {"product_id": "P006", "name": "Samsung Galaxy S24 Ultra", "price": 129999, "category": "Smartphone", "image": "/images/galaxy.jpg"},
        ]
        await product_collection.insert_many(products)
        print("Sample products seeded.")

async def get_all_products() -> List[Dict[str, Any]]:
    product_collection = await get_product_collection()
    products = await product_collection.find().to_list(None)
    for p in products:
        p["_id"] = str(p["_id"])
    return products
