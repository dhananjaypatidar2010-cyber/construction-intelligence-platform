"""Strict JSON data contracts shared by the backend and the React frontend.

Every AI response is validated against one of these models before it is
returned, so the UI never receives malformed or unexpected data.
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field

Severity = Literal["low", "medium", "high", "critical"]


# ---------- Safety monitoring ----------
class SafetyFinding(BaseModel):
    label: str
    severity: Severity
    description: str
    recommendation: str


class SafetyResult(BaseModel):
    overall_risk: Severity
    safety_score: int = Field(ge=0, le=100)
    ppe_summary: str
    findings: list[SafetyFinding]
    immediate_actions: list[str]


# ---------- Crack detection ----------
class CrackResult(BaseModel):
    crack_detected: bool
    crack_type: str  # hairline, shrinkage, settlement, structural, none
    severity: Severity
    estimated_width_mm: Optional[float] = None
    structural_risk: str
    probable_causes: list[str]
    recommended_actions: list[str]
    monitoring_interval_days: int = Field(ge=0)


# ---------- Real estate valuation ----------
class ValuationRequest(BaseModel):
    location: str
    property_type: str = "apartment"
    area_sqft: float = Field(gt=0)
    bedrooms: int = Field(ge=0, default=2)
    age_years: int = Field(ge=0, default=0)
    condition: Literal["poor", "average", "good", "excellent"] = "good"
    amenities: list[str] = []
    notes: str = ""


class ValuationResult(BaseModel):
    currency: str
    estimated_value_low: float
    estimated_value_high: float
    price_per_sqft: float
    confidence: Literal["low", "medium", "high"]
    key_factors: list[str]
    assumptions: list[str]
    disclaimer: str


# ---------- Project planning ----------
class PlanningRequest(BaseModel):
    project_name: str
    project_type: str = "residential building"
    area_sqft: float = Field(gt=0)
    budget: float = Field(gt=0)
    duration_weeks: int = Field(gt=0, default=52)
    location: str = ""
    constraints: str = ""


class Phase(BaseModel):
    name: str
    duration_weeks: int
    cost_share_pct: float
    tasks: list[str]
    milestones: list[str]


class Risk(BaseModel):
    risk: str
    likelihood: Severity
    mitigation: str


class PlanningResult(BaseModel):
    summary: str
    total_estimated_cost: float
    phases: list[Phase]
    key_resources: list[str]
    risks: list[Risk]


# ---------- Daily site assistant ----------
class DailyRequest(BaseModel):
    tasks_today: list[str]
    crew_size: int = Field(ge=1, default=10)
    notes: str = ""
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)


class WeatherSnapshot(BaseModel):
    temperature_c: float
    wind_kmh: float
    precipitation_mm: float
    conditions: str


class DailyResult(BaseModel):
    briefing: str
    priorities: list[str]
    safety_reminders: list[str]
    material_checklist: list[str]
    risks: list[str]
    weather: Optional[WeatherSnapshot] = None


# ---------- Weather-aware advisory ----------
class WeatherRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    activity: str = "general site work"


class WeatherAdvisory(BaseModel):
    work_recommendation: Literal["proceed", "caution", "halt"]
    advisory: str
    activities_to_avoid: list[str]
    precautions: list[str]
    weather: Optional[WeatherSnapshot] = None


# ---------- Construction knowledge assistant ----------
class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class KnowledgeRequest(BaseModel):
    question: str = Field(min_length=3)
    history: list[ChatTurn] = []


class KnowledgeResult(BaseModel):
    answer: str
    references: list[str]
    follow_up_questions: list[str]
