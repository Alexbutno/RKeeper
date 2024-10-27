import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.recipes.schemas import Recipe, RecipeID
from src.utils import decode_jwt_token, get_mongo_db_manager

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/get_all")
async def get_recipes(token: str = Depends(oauth2_scheme)):
    token_payload = await decode_jwt_token(token)
    user_id = token_payload["user_id"]
    db_manager_mongo = await get_mongo_db_manager()
    recipes = await db_manager_mongo.user_get_recipes(user_id)
    return recipes


@router.post("/add")
async def add_recipe(recipe: Recipe, token: str = Depends(oauth2_scheme)):
    token_payload = await decode_jwt_token(token)
    user_id = token_payload["user_id"]
    db_manager_mongo = await get_mongo_db_manager()
    await db_manager_mongo.user_add_recipe(user_id, recipe)
    return {"status": "recipe successfully added"}


@router.post("/delete")
async def delete_recipe(recipe_id: RecipeID, token: str = Depends(oauth2_scheme)):
    token_payload = await decode_jwt_token(token)
    recipe_id = str(recipe_id.model_dump()["recipe_id"])
    user_id = token_payload["user_id"]
    db_manager_mongo = await get_mongo_db_manager()
    await db_manager_mongo.user_delete_recipe(user_id, recipe_id)
    return {"status": "recipe successfully deleted"}


@router.post("/update")
async def update_recipe(recipe_id: RecipeID, recipe: Recipe, token: str = Depends(oauth2_scheme)):
    token_payload = await decode_jwt_token(token)
    recipe_id = str(recipe_id.model_dump()["recipe_id"])

    user_id = token_payload["user_id"]
    db_manager_mongo = await get_mongo_db_manager()

    if not await db_manager_mongo.check_if_recipe_exists(user_id, recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")

    await db_manager_mongo.user_update_recipe(user_id, recipe_id, recipe)

    return {"message": "Recipe successfully updated"}

