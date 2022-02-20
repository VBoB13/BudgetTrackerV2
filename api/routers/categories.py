from fastapi import APIRouter, HTTPException

from ..objects.categories import Category
from ..typing.models import CategoryOut, CategoriesOut
from ..db.controller import query_db, ControllerError

router = APIRouter(
    prefix='/categories',
    tags=["categories"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.get("/all", response_model=CategoriesOut)
async def get_all_categories():
    sql = Category.get_all()
    results = query_db(sql)
    output_list = []
    for category in results:
        output_list.append(dict(Category(category)))

    return {"categories": output_list}
