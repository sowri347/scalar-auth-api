from fastapi import APIRouter, HTTPException
from app.core.product_collection import get_all_products, seed_products

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

@router.on_event("startup")
async def startup_seed():
    await seed_products()

@router.get("/", response_model=list)
async def list_products():
    products = await get_all_products()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products
