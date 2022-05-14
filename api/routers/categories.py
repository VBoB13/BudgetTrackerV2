from pprint import pprint
from traceback import print_tb
from colorama import Fore, Style
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
            "color": "Red"
        },
        {
            "id": 6,
            "name": "Kitties",
            "color": "LightBlue"
        },
        {
            "id": 7,
            "name": "Others",
            "color": "LightGray"
        }
    ]
    try:
        sql = Category.get_all()
        results = query_db(sql)
        for category in results:
            output_list.append(dict(Category(category)))
    except Exception as err:
        print(Fore.RED, "ERROR:", Style.RESET_ALL)
        print(Fore.YELLOW, err, Style.RESET_ALL)
        # print_tb(err.__traceback__)
        print("\n", Fore.YELLOW, "Categories:", Style.RESET_ALL)
        pprint(output_list)
        return {"categories": output_list}

    print("Categories:")
    pprint(output_list)
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
