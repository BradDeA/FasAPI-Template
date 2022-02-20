from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {}


@app.get("/")
def home_page():
    return {"Home": "Page"}


@app.get("/item/{item_id}")
def get_item(item_id: int = Path(None, description="ID of the item you want to view", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail='Item ID does not exist')

    return inventory[item_id]


@app.get("/get-name")
def get_item(name: str = Query(None)):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail='Item name not found')


@app.post('/create-item/{item_id}')
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail='Item ID exists')

    inventory[item_id] = item
    return inventory[item_id]


@app.put('/update-item/{item_id}')
def update_item(item_id: int, item: ItemUpdate):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail='Item ID does not exist')

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]


@app.delete('/delete-item')
def delete_item(item_id: int = Query(..., description='The ID for the item to delete', gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=400, detail='Item ID not exsist')

    del inventory[item_id]
    return {'Item': 'Deleted'}
