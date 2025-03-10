from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ... import crud, schemas

router = APIRouter()

@router.get('/', response_model=List[schemas.PriceModel])
async def prices_info(first_n: Optional[int] = None, db: Session = Depends(get_db)):
    prices = crud.get_prices(db, first_n)
    return prices

@router.get('/{price_id}', response_model=schemas.PriceModel)
async def get_price(price_id: int, db: Session = Depends(get_db)):
    price = crud.get_price(db, price_id)
    if price is None:
        raise HTTPException(status_code=404, detail="Price not found")
    return price

@router.post('/', response_model=schemas.PriceModel)
async def create_price(price: schemas.PriceCreate, db: Session = Depends(get_db)):
    return crud.create_price(db, price)