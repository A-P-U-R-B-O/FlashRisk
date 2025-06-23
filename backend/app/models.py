from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Literal, Annotated
from datetime import datetime

# --- Disaster Event Models ---

class EarthquakeEvent(BaseModel):
    id: str = Field(..., description="Unique USGS event ID")
    place: str
    magnitude: float = Field(..., alias="mag")
    time: datetime
    url: HttpUrl
    depth_km: Optional[float] = Field(None, description="Depth in kilometers")
    latitude: Optional[float]
    longitude: Optional[float]
    felt: Optional[int] = Field(None, description="Number of reports from people who felt it")
    tsunami: Optional[bool] = Field(None, description="Whether a tsunami was triggered")
    updated: Optional[datetime]

class WeatherAlert(BaseModel):
    id: str = Field(..., description="Unique alert ID")
    event: str = Field(..., description="Type of weather event (e.g., Tornado Warning)")
    area_desc: str = Field(..., alias="areaDesc")
    severity: Literal["Extreme", "Severe", "Moderate", "Minor", "Unknown"]
    headline: str
    description: str
    url: Optional[HttpUrl]
    sent: Optional[datetime]
    effective: Optional[datetime]
    expires: Optional[datetime]

class SocialSignal(BaseModel):
    id: str
    platform: Literal["twitter", "facebook", "reddit"]
    text: str
    author: str
    timestamp: datetime
    location: Optional[str]
    url: Optional[HttpUrl]
    confidence: Optional[float] = Field(None, description="ML confidence score for disaster relevance")

# --- Notification Models ---

class Notification(BaseModel):
    id: str
    type: Literal["sms", "email", "push", "webhook"]
    recipient: str
    title: str
    message: str
    sent_at: datetime
    status: Literal["pending", "sent", "failed"]
    event_id: Optional[str] = Field(None, description="Associated disaster event ID")

# --- User Models (for future expansion) ---

class UserProfile(BaseModel):
    id: str
    name: Optional[str]
    email: Optional[str]
    phone: Optional[Annotated[str, Field(pattern=r"^\+?[1-9]\d{1,14}$")]]
    preferences: Optional[List[str]] = Field(None, description="Types of alerts the user wants to receive")
    created_at: datetime
    is_active: bool = True

# --- API Response Models ---

class EarthquakeListResponse(BaseModel):
    earthquakes: List[EarthquakeEvent]

class WeatherAlertListResponse(BaseModel):
    alerts: List[WeatherAlert]

class NotificationListResponse(BaseModel):
    notifications: List[Notification]

# --- Utility Schemas ---

class HealthCheckResponse(BaseModel):
    status: Literal["ok"]
    timestamp: datetime
