"""Sample responses used when LLM_PROVIDER=mock."""
from .schemas import *  # noqa: F401,F403

SAFETY = SafetyResult(
    overall_risk="high", safety_score=54,
    ppe_summary="2 of 4 visible workers wear hard hats; no high-visibility vests on the scaffold level.",
    findings=[
        SafetyFinding(label="Missing hard hat", severity="high",
                      description="A worker near the formwork is not wearing head protection.",
                      recommendation="Stop work for that worker until a helmet is worn."),
        SafetyFinding(label="Unprotected edge", severity="critical",
                      description="Open slab edge without guardrail or toe board.",
                      recommendation="Install guardrails or a safety net before further work."),
        SafetyFinding(label="Material stacking", severity="medium",
                      description="Bricks are stacked above recommended height near a walkway.",
                      recommendation="Restack to a stable height and keep walkways clear."),
    ],
    immediate_actions=["Cordon off the open edge", "Issue PPE to all workers", "Hold a toolbox talk before the next shift"],
)

CRACK = CrackResult(
    crack_detected=True, crack_type="diagonal settlement", severity="medium",
    estimated_width_mm=2.5,
    structural_risk="Possible differential settlement; not immediately dangerous but needs engineer review.",
    probable_causes=["Differential foundation settlement", "Poor soil compaction", "Water ingress near the footing"],
    recommended_actions=["Install crack gauges at both ends", "Fix drainage near the wall", "Have a structural engineer inspect within 2 weeks"],
    monitoring_interval_days=14,
)

VALUATION = ValuationResult(
    currency="INR", estimated_value_low=6200000, estimated_value_high=7400000, price_per_sqft=6800,
    confidence="medium",
    key_factors=["Location demand and connectivity", "Good condition, low building age", "Amenities such as parking and security"],
    assumptions=["Comparable sales within 2 km averaged ₹6,000–7,500 per sq ft", "No legal or title issues"],
    disclaimer="Indicative estimate only. Get a certified valuer's report before any transaction.",
)

PLANNING = PlanningResult(
    summary="A phased plan covering approvals, foundation, structure, services and finishing with contingency built in.",
    total_estimated_cost=0,
    phases=[
        Phase(name="Pre-construction", duration_weeks=6, cost_share_pct=5,
              tasks=["Soil test", "Drawings and approvals", "Contractor selection"], milestones=["Permits received"]),
        Phase(name="Foundation and substructure", duration_weeks=10, cost_share_pct=20,
              tasks=["Excavation", "Footings and plinth beam", "Waterproofing"], milestones=["Plinth complete"]),
        Phase(name="Superstructure", duration_weeks=18, cost_share_pct=35,
              tasks=["Columns and slabs", "Masonry", "Roof slab"], milestones=["Structure topped out"]),
        Phase(name="MEP and finishing", duration_weeks=18, cost_share_pct=40,
              tasks=["Electrical and plumbing", "Plaster and flooring", "Painting and fixtures"], milestones=["Handover"]),
    ],
    key_resources=["Site engineer", "Mason crew of 12", "Tower crane or hoist", "Ready-mix concrete supplier"],
    risks=[
        Risk(risk="Monsoon delays to foundation work", likelihood="medium", mitigation="Schedule excavation outside peak rain; keep dewatering pumps on site."),
        Risk(risk="Material price escalation", likelihood="high", mitigation="Bulk-buy steel and cement early; add a 7% contingency."),
    ],
)

DAILY = DailyResult(
    briefing="Focus on slab concreting today; keep the crew clear of the crane swing zone.",
    priorities=["Complete rebar inspection before the pour", "Confirm concrete delivery slots", "Curing setup for yesterday's pour"],
    safety_reminders=["Helmets and vests at all times", "Check scaffold tags", "Keep fire extinguisher near welding"],
    material_checklist=["Ready-mix concrete 24 m³", "Vibrators and spare needle", "Curing compound", "Formwork oil"],
    risks=["Late concrete trucks", "Wind affecting crane lifts"],
)

WEATHER = WeatherAdvisory(
    work_recommendation="proceed",
    advisory="Conditions are suitable for normal site work. Monitor wind if crane lifts are planned.",
    activities_to_avoid=["Unsecured sheet roofing in gusts"],
    precautions=["Hydrate regularly", "Cover cement and fresh concrete if rain develops"],
)

KNOWLEDGE = KnowledgeResult(
    answer="For slabs in normal conditions, cure for at least 7 days with ordinary Portland cement (10 days if blended cement or hot weather). Keep the surface continuously moist by ponding, wet hessian or curing compound.",
    references=["IS 456:2000 clause 13.5", "ACI 308R guide to curing concrete"],
    follow_up_questions=["How do I cure concrete in hot weather?", "When can I remove slab formwork?"],
)
