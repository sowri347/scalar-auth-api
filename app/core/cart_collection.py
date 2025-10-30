from bson import ObjectId
from typing import List, Dict, Any
from app.core.database import get_database

CART_COLLECTION = "cart"

def convert_objectid(data):
    """Recursively convert ObjectId to string for JSON serialization"""
    if isinstance(data, list):
        return [convert_objectid(i) for i in data]
    if isinstance(data, dict):
        return {k: convert_objectid(v) for k, v in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data

async def get_cart_collection():
    db = get_database()
    return db[CART_COLLECTION]

async def get_cart_by_user(username: str) -> Dict[str, Any]:
    cart_collection = await get_cart_collection()
    cart = await cart_collection.find_one({"username": username})
    if not cart:
        new_cart = {"username": username, "items": []}
        await cart_collection.insert_one(new_cart)
        return new_cart
    return convert_objectid(cart)

async def add_to_cart(username: str, product: Dict[str, Any]):
    cart_collection = await get_cart_collection()
    cart = await get_cart_by_user(username)

    for item in cart["items"]:
        if item["product_id"] == product["product_id"]:
            item["quantity"] += product.get("quantity", 1)
            break
    else:
        cart["items"].append(product)

    await cart_collection.update_one(
        {"username": username},
        {"$set": {"items": cart["items"]}}
    )

    return {"message": "Product added to cart", "cart": convert_objectid(cart)}

async def remove_from_cart(username: str, product_id: str):
    cart_collection = await get_cart_collection()
    cart = await get_cart_by_user(username)
    updated_items = [item for item in cart["items"] if item["product_id"] != product_id]

    await cart_collection.update_one(
        {"username": username},
        {"$set": {"items": updated_items}}
    )

    return {"message": "Product removed", "cart": convert_objectid({"items": updated_items})}

async def clear_cart(username: str):
    cart_collection = await get_cart_collection()
    await cart_collection.update_one(
        {"username": username},
        {"$set": {"items": []}}
    )
    return {"message": "Cart cleared"}
