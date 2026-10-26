from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from .. import mocks
from ..config import settings
from ..llm import generate_json, read_image
from ..schemas import CrackResult, SafetyResult

router = APIRouter(prefix="/api", tags=["image analysis"])


@router.post("/safety/analyze", response_model=SafetyResult)
async def analyze_safety(image: UploadFile = File(...), notes: Optional[str] = Form("")):
    img = await read_image(image, settings.max_image_mb)
    task = (
        "Inspect this construction site photo for safety hazards: missing PPE (helmets, vests, "
        "harnesses, boots), unprotected edges, unsafe scaffolding, poor housekeeping, electrical "
        "hazards, unsafe material storage, and machinery proximity. Score overall safety 0-100 "
        f"(100 = safe). Site notes from the user: {notes or 'none'}."
    )
    return await generate_json(task, SafetyResult, mocks.SAFETY, img)


@router.post("/cracks/analyze", response_model=CrackResult)
async def analyze_crack(image: UploadFile = File(...), element: Optional[str] = Form("wall")):
    img = await read_image(image, settings.max_image_mb)
    task = (
        f"Analyse this photo of a {element or 'wall'} for cracks. Classify the crack type, estimate "
        "width in mm if a scale is visible (otherwise null), judge severity and structural risk, "
        "list probable causes, recommend actions, and suggest a monitoring interval in days. "
        "If no crack is visible set crack_detected=false, crack_type='none', severity='low'."
    )
    return await generate_json(task, CrackResult, mocks.CRACK, img)
