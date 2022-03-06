from fastapi import APIRouter, HTTPException
from typing import List

from ..Utils.exceptions import ControllerError

from ..db.controller import query_db
from ..typing.models import IncomeIn, IncomeOut, IncomesOut
from ..objects.incomes import Income

router = APIRouter(
    prefix='/incomes',
    tags=["incomes"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.get("/get_all", description="Shows all incomes registered in the DB.", response_model=IncomesOut)
async def get_all_incomes():
    sql = Income.get_all_incomes()
    incomes = [Income(item) for item in query_db(sql)]
    return {"incomes": incomes}


@router.post("/add_income", description="Add income.")
async def add_income(income: IncomeIn):
    sql = Income.add_income(income.user, income.amount,
                            income.currency, income.date)
    try:
        query_db(sql, True)
    except ControllerError as err:
        raise HTTPException(500, "Could not add income to DB!") from err
    except Exception as err:
        raise HTTPException(500,
                            "Something went wrong when adding income to DB!") from err

    return await get_all_incomes()
