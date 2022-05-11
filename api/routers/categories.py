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
    output_list = [
        {
            "id": 1,
            "name": "Food",
            "color": "Green"
        },
        {
            "id": 2,
            "name": "Rent & Utilities",
            "color": "Gray"
        },
        {
            "id": 3,
            "name": "Medical",
            "color": "Pink"
        },
        {
            "id": 4,
            "name": "Leisure",
            "color": "Blue"
        },
        {
            "id": 5,
            "name": "Travel",
            "color": "LightBlue"
        },
        {
            "id": 6,
            "name": "Others",
            "color": "LightGray"
        }
    ]
    try:
        sql = Category.get_all()
        results = query_db(sql)
        for category in results:
            output_list.append(dict(Category(category)))
    except ControllerError as err:
        return {"categories": output_list}

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
