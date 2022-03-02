from fastapi import APIRouter, HTTPException

from ..objects.stores import Store
from ..typing.models import StoreIn, StoreOut, StoresOut
from ..db.controller import query_db, ControllerError

router = APIRouter(
    prefix='/stores',
    tags=["stores"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.get("/get_all", description="Show all the registered stores in the database.", response_model=StoresOut)
async def get_all_stores():
    sql = Store.get_all_stores()
    try:
        stores = [Store(item) for item in query_db(sql)]
    except ControllerError as err:
        raise HTTPException(
            500, "Could not retrieve stores from database!") from err

    return {"stores": stores}


@router.post("/add", description="Add a single store to the database.", response_model=StoreOut)
async def add_store(store: StoreIn):
    sql = Store.add_store(store.name)
    try:
        query_db(sql, True)
    except ControllerError as err:
        raise HTTPException(
            500, "Could not insert new store ({}) into database!".format(store.name)) from err
    else:
        sql = Store.get_store(store.name)
        try:
            result_store = Store(query_db(sql)[0])
        except ControllerError as err:
            raise HTTPException(
                500, "Could not retrieve the newly added store ({}) from database!".format(store.name)) from err
        else:
            return dict(result_store)
