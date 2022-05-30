from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

import json

from ..typing.models import StatsImage
from ..objects.stats import Stats

router = APIRouter(
    prefix='/stats',
    tags=["stats"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.post("/get_daily_category_sum", description="Shows sums of all transactions for each category each day.")
async def get_daily_category_sums(img: StatsImage):
    stats = Stats()
    stats.get_category_sums_per_date()
    print(img)
    if img.yes:
        graph_bytes = stats.create_bytes_categories(plot="line")
        return StreamingResponse(graph_bytes, media_type="image/png")
    return json.loads(stats.df.to_json())


@router.post("/get_category_sum_ratio", description="Shows a piechart of how much the sum for each category is.")
async def get_category_sum_ratio(img: StatsImage):
    stats = Stats()
    stats.get_category_sums()
    if img.yes:
        graph_bytes = stats.create_bytes_categories(plot="pie")
        return StreamingResponse(graph_bytes, media_type="image/png")
    return json.loads(stats.df.to_json())


@router.post("/get_meal_avgs", description="Shows the average cost of each meal; Breakfast, Lunch and Dinner.")
async def get_meal_avgs(img: StatsImage):
    stats = Stats()
    stats.get_meal_avgs()
    if img.yes:
        graph_bytes = stats.create_bytes_categories(plot="bar")
        return StreamingResponse(graph_bytes, media_type="image/png")
    return json.loads(stats.df.to_json())
