from datetime import datetime  # Import datetime for timestamps.  
from typing import Dict, Optional  # Import type hints.  

from pydantic import BaseModel, Field  # Import Pydantic base classes.  


class SecurityEvent(BaseModel):  # Define the incoming event shape.  
    event_id: str = Field(..., description="Unique event id.")  # Unique id for event tracking.  
    timestamp: datetime = Field(..., description="Event time in ISO format.")  # Event time.  
    source: str = Field(..., description="Event source system.")  # Source application or tool.  
    event_type: str = Field(..., description="Type of event.")  # Event category.  
    user_id: Optional[str] = Field(default=None, description="Optional user id.")  # User if known.  
    ip_address: Optional[str] = Field(default=None, description="Optional source IP.")  # IP if known.  
    severity: str = Field(..., description="Input severity.")  # Initial event severity.  
    message: str = Field(..., description="Human-readable event message.")  # Event text.  
    metadata: Dict[str, str] = Field(default_factory=dict, description="Extra event fields.")  # Key-value metadata.  


class DetectionResult(BaseModel):  # Define the output of the detection engine.  
    event_id: str  # Reference the original event id.  
    is_suspicious: bool  # Tell whether the event looks suspicious.  
    threat_type: str  # Name the likely threat.  
    risk_score: int  # Score from 0 to 100.  
    vulnerability_reason: str  # Explain what weakness was noticed.  
    next_action: str  # Recommend what the operator should do.  


class TriageResult(BaseModel):  # Define the final AI triage output.  
    event_id: str  # Keep the original event id.  
    summary: str  # Short explanation of the incident.  
    business_impact: str  # Explain why it matters.  
    operator_action: str  # Human action recommendation.
