from fastapi import APIRouter

from .. import mocks
from ..llm import generate_json
from ..schemas import (DailyRequest, DailyResult, KnowledgeRequest, KnowledgeResult,
                       WeatherAdvisory, WeatherRequest)
from ..weather import fetch_weather, rule_based_recommendation

router = APIRouter(prefix="/api", tags=["assistant"])

ORDER = {"proceed": 0, "caution": 1, "halt": 2}


@router.post("/assistant/daily", response_model=DailyResult)
async def daily(req: DailyRequest):
    weather = None
    if req.latitude is not None and req.longitude is not None:
        weather = await fetch_weather(req.latitude, req.longitude)
    task = (
        "Prepare a morning site briefing for a construction supervisor: priorities, safety reminders, "
        "a material checklist and risks for today.\n"
        f"Tasks: {req.tasks_today}\nCrew size: {req.crew_size}\nNotes: {req.notes or 'none'}\n"
        f"Weather: {weather.model_dump_json() if weather else 'unavailable'}"
    )
    result = await generate_json(task, DailyResult, mocks.DAILY)
    return result.model_copy(update={"weather": weather})


@router.post("/advisory/weather", response_model=WeatherAdvisory)
async def weather_advisory(req: WeatherRequest):
    weather = await fetch_weather(req.latitude, req.longitude)
    if weather is None:
        from fastapi import HTTPException
        raise HTTPException(502, "Weather service is unavailable. Try again shortly.")
    floor = rule_based_recommendation(weather)
    task = (
        f"Give a weather-aware advisory for the activity '{req.activity}'. Current weather: "
        f"{weather.model_dump_json()}. Rule-based minimum recommendation: {floor}."
    )
    mock = mocks.WEATHER.model_copy(update={"work_recommendation": floor})
    result = await generate_json(task, WeatherAdvisory, mock)
    # Never let the model be more lenient than the deterministic safety rules.
    rec = result.work_recommendation if ORDER[result.work_recommendation] >= ORDER[floor] else floor
    return result.model_copy(update={"work_recommendation": rec, "weather": weather})


@router.post("/knowledge/ask", response_model=KnowledgeResult)
async def knowledge(req: KnowledgeRequest):
    history = "\n".join(f"{t.role}: {t.content}" for t in req.history[-8:])
    task = (
        "Answer this construction question accurately and practically. Cite relevant codes or standards "
        "(e.g. IS, ACI, Eurocode, OSHA) in references only if you are confident they exist; otherwise "
        f"leave references empty. Suggest 2-3 follow-up questions.\nHistory:\n{history or 'none'}\n"
        f"Question: {req.question}"
    )
    return await generate_json(task, KnowledgeResult, mocks.KNOWLEDGE)
