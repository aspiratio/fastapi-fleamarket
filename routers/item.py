from fastapi import APIRouter, Path, Query, HTTPException
from cruds import item as item_cruds
from schemas import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])  # prefix=共通のパス, tags=[ルーターの名前]


@router.get("", response_model=list[ItemResponse])
async def find_all():
    return item_cruds.find_all()


@router.get("/{id}", response_model=ItemResponse)
async def find_by_id(id: int = Path(gt=0)):
    found_item = item_cruds.find_by_id(id)
    if not found_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return found_item


@router.get("/", response_model=list[ItemResponse])  # /itemsが上書きされないように末尾に/を入れている
async def find_by_name(name: str = Query(min_length=2, max_length=20)):
    return item_cruds.find_by_name(name)


@router.post("", response_model=ItemResponse)
async def create(item_create: ItemCreate):
    return item_cruds.create(item_create)


@router.put("/{id}", response_model=ItemResponse)
async def update(item_update: ItemUpdate, id: int = Path(gt=0)):
    updated_item = item_cruds.update(id, item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not updated")
    return updated_item


@router.delete("/{id}", response_model=ItemResponse)
async def delete(id: int = Path(gt=0)):
    deleted_item = item_cruds.delete(id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not deleted")
    return deleted_item
