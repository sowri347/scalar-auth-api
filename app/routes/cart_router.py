from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.cart_collection import (
    get_cart_by_user,
    add_to_cart,
    remove_from_cart,
    clear_cart
)
from app.core.auth_dependencies import get_current_user  
from app.schema.auth import UserInDB

router = APIRouter(prefix="/api/v1/cart", tags=["Cart"])


@router.get("/", response_model=Dict[str, Any])
async def get_user_cart(current_user: UserInDB = Depends(get_current_user)):
    username = current_user.username 
    cart = await get_cart_by_user(username)
    return {"cart": cart}


@router.post("/add", response_model=Dict[str, Any])
async def add_item_to_cart(product: Dict[str, Any], current_user: UserInDB = Depends(get_current_user)):
    username = current_user.username  
    if not product.get("product_id"):
        raise HTTPException(status_code=400, detail="product_id is required")
    return await add_to_cart(username, product)


@router.delete("/remove/{product_id}", response_model=Dict[str, Any])
async def remove_item_from_cart(product_id: str, current_user: UserInDB = Depends(get_current_user)):
    username = current_user.username  
    return await remove_from_cart(username, product_id)


@router.delete("/clear", response_model=Dict[str, Any])
async def clear_user_cart(current_user: UserInDB = Depends(get_current_user)):
    username = current_user.username  
    return await clear_cart(username)
