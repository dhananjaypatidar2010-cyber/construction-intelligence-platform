from fastapi import APIRouter

from .. import mocks
from ..llm import generate_json
from ..schemas import PlanningRequest, PlanningResult, ValuationRequest, ValuationResult

router = APIRouter(prefix="/api", tags=["planning and valuation"])


@router.post("/valuation", response_model=ValuationResult)
async def valuation(req: ValuationRequest):
    task = (
        "Estimate the market value range of this property. State the local currency, a low and high "
        "value, price per sq ft, confidence, key value drivers and your assumptions. Include a short "
        f"disclaimer that this is indicative.\nProperty: {req.model_dump_json()}"
    )
    mock = mocks.VALUATION.model_copy(
        update={
            "estimated_value_low": round(req.area_sqft * 6000),
            "estimated_value_high": round(req.area_sqft * 7500),
            "price_per_sqft": 6750,
        }
    )
    return await generate_json(task, ValuationResult, mock)


@router.post("/planning", response_model=PlanningResult)
async def planning(req: PlanningRequest):
    task = (
        "Create a construction project plan with sequential phases. Phase cost_share_pct values must "
        "sum to about 100 and phase durations to about the total duration. total_estimated_cost must "
        f"stay close to the budget. Include risks and key resources.\nProject: {req.model_dump_json()}"
    )
    mock = mocks.PLANNING.model_copy(update={"total_estimated_cost": req.budget})
    result = await generate_json(task, PlanningResult, mock)
    return result
