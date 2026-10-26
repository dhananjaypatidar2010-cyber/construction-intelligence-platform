"""Live weather from Open-Meteo (free, no API key)."""
import httpx

from .schemas import WeatherSnapshot

WMO = {
    0: "Clear sky", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain", 71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Heavy showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Severe thunderstorm with hail",
}


async def fetch_weather(lat: float, lon: float) -> "WeatherSnapshot | None":
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,precipitation,wind_speed_10m,weather_code",
                },
            )
        r.raise_for_status()
        cur = r.json()["current"]
        return WeatherSnapshot(
            temperature_c=cur["temperature_2m"],
            wind_kmh=cur["wind_speed_10m"],
            precipitation_mm=cur["precipitation"],
            conditions=WMO.get(cur["weather_code"], f"Code {cur['weather_code']}"),
        )
    except Exception:
        return None


def rule_based_recommendation(w: WeatherSnapshot) -> str:
    """Deterministic safety floor; applied even if the LLM is lenient."""
    if w.wind_kmh >= 60 or "hail" in w.conditions.lower() or "thunder" in w.conditions.lower():
        return "halt"
    if w.wind_kmh >= 40 or w.precipitation_mm >= 2.5 or w.temperature_c >= 40 or w.temperature_c <= 0:
        return "caution"
    return "proceed"
