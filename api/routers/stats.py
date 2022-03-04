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
    stats.get_category_sums()
    if img.yes:
        graph_bytes = stats.create_bytes()
        return StreamingResponse(graph_bytes, media_type="image/png")
    return json.loads(stats.df.to_json())
