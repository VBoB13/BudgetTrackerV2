from fastapi import APIRouter, HTTPException

from ..objects.categories import Category
from ..typing.models import CategoriesOut, CategoryIn
from ..db.controller import query_db, ControllerError

router = APIRouter(
    prefix='/categories',
    tags=["categories"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.get("/get_all", response_model=CategoriesOut)
async def get_all_categories():
    sql = Category.get_all()
    results = query_db(sql)
    output_list = []
    for category in results:
        output_list.append(dict(Category(category)))

    return {"categories": output_list}


@router.post("/add", description="Add a category.")
async def add_category(category: CategoryIn):
    sql = Category.add_category(category.name, category.color)
    try:
        results = query_db(sql, True)
        if results:
            return {
                "message": "Success!"
            }
    except Exception as err:
        raise HTTPException(500, str(err))
