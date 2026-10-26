"""Multimodal LLM gateway.

One function, `generate_json`, sends text (and optionally an image) to the
configured provider, extracts JSON from the reply, and validates it against a
Pydantic model. If validation fails it retries once with the error message.
The `mock` provider returns canned sample data so the app runs without a key.
"""
import base64
import json
import re
from typing import Optional, Type, TypeVar

import httpx
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError

from .config import settings

T = TypeVar("T", bound=BaseModel)

SYSTEM_PROMPT = (
    "You are an expert construction engineer, safety officer, quantity surveyor and "
    "real estate analyst embedded in a construction intelligence platform. "
    "Respond with ONE JSON object only: no markdown fences, no commentary. "
    "The JSON must match the supplied JSON schema exactly (same keys, same types, "
    "enum values spelled exactly). Never invent fields. Be concrete and practical. "
    "When a request lacks data, state your assumptions inside the JSON fields."
)


class Image(BaseModel):
    data: bytes
    media_type: str


def _extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found in model reply")
    return json.loads(text[start : end + 1])


async def _call_anthropic(prompt: str, image: Optional[Image]) -> str:
    content: list[dict] = []
    if image:
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image.media_type,
                    "data": base64.b64encode(image.data).decode(),
                },
            }
        )
    content.append({"type": "text", "text": prompt})
    async with httpx.AsyncClient(timeout=90) as client:
        r = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": settings.anthropic_model,
                "max_tokens": 2500,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": content}],
            },
        )
    r.raise_for_status()
    return "".join(b.get("text", "") for b in r.json()["content"])


async def _call_gemini(prompt: str, image: Optional[Image]) -> str:
    parts: list[dict] = [{"text": prompt}]
    if image:
        parts.append(
            {"inline_data": {"mime_type": image.media_type, "data": base64.b64encode(image.data).decode()}}
        )
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.gemini_model}:generateContent"
    )
    async with httpx.AsyncClient(timeout=90) as client:
        r = await client.post(
            url,
            headers={"x-goog-api-key": settings.gemini_api_key},
            json={
                "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "contents": [{"role": "user", "parts": parts}],
                "generationConfig": {"responseMimeType": "application/json"},
            },
        )
    r.raise_for_status()
    return "".join(p.get("text", "") for p in r.json()["candidates"][0]["content"]["parts"])


async def generate_json(
    task: str,
    model_cls: Type[T],
    mock: T,
    image: Optional[Image] = None,
) -> T:
    provider = settings.llm_provider.lower()
    if provider == "mock":
        return mock

    if provider == "anthropic" and not settings.anthropic_api_key:
        raise HTTPException(500, "ANTHROPIC_API_KEY is not set in backend/.env")
    if provider == "gemini" and not settings.gemini_api_key:
        raise HTTPException(500, "GEMINI_API_KEY is not set in backend/.env")
    if provider not in ("anthropic", "gemini"):
        raise HTTPException(500, f"Unknown LLM_PROVIDER '{provider}'")

    caller = _call_anthropic if provider == "anthropic" else _call_gemini
    schema = json.dumps(model_cls.model_json_schema())
    prompt = f"{task}\n\nJSON schema to follow:\n{schema}"

    last_error = ""
    for attempt in range(2):
        try:
            reply = await caller(prompt if not last_error else f"{prompt}\n\nYour previous reply was invalid: {last_error}\nReturn corrected JSON only.", image)
            return model_cls.model_validate(_extract_json(reply))
        except (ValidationError, ValueError) as e:
            last_error = str(e)[:500]
        except httpx.HTTPStatusError as e:
            raise HTTPException(502, f"{provider} API error {e.response.status_code}: {e.response.text[:300]}")
        except httpx.HTTPError as e:
            raise HTTPException(502, f"Could not reach {provider}: {e}")
    raise HTTPException(502, f"Model returned data that did not match the contract: {last_error}")


async def read_image(upload, max_mb: int) -> Image:
    allowed = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    if upload.content_type not in allowed:
        raise HTTPException(415, "Upload a JPEG, PNG, WebP or GIF image.")
    data = await upload.read()
    if len(data) > max_mb * 1024 * 1024:
        raise HTTPException(413, f"Image is larger than {max_mb} MB.")
    if not data:
        raise HTTPException(400, "The uploaded image is empty.")
    return Image(data=data, media_type=upload.content_type)
