from fastapi import APIRouter, HTTPException

from ..objects.stats import Stats

router = APIRouter(
    prefix='/stats',
    tags=["stats"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.post("/get_daily_category_sum", description="Shows sums of all transactions for each category each day.")
async def get_daily_category_sums():
    stats = Stats()
    return stats.get_category_sums()
