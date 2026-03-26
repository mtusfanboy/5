from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"}
}
_next_id = 2


class UserCreate(BaseModel):
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str
    email: str


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@router.post("/users/", status_code=201)
async def create_user(user: UserCreate):
    global _next_id
    new_user = {"id": _next_id, "name": user.name, "email": user.email}
    users_db[_next_id] = new_user
    _next_id += 1
    return new_user


@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id].update({"name": user.name, "email": user.email})
    return users_db[user_id]


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
