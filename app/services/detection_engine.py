from app.models import DetectionResult, SecurityEvent  # Import models.  
from app.services.threat_model import map_threat  # Import threat mapping helper.  
from app.services.vulnerability_analysis import analyze_vulnerability  # Import vulnerability helper.  


def score_event(event: SecurityEvent, threat_type: str) -> int:  # Create a simple risk score.  
    score = 30  # Start with a base risk score.  
    if event.severity.lower() == "high":  # If source severity is high.  
        score += 30  # Add more risk.  
    if threat_type in {"SQL Injection", "Prompt Injection", "Cross-Site Scripting"}:  # Check major app attack types.  
        score += 30  # Add more risk.  
    if threat_type == "Brute Force Attempt":  # Check brute force case.  
        score += 20  # Add a smaller boost.  
    return min(score, 100)  # Cap the score at 100.  


def detect_event(event: SecurityEvent) -> DetectionResult:  # Run the simple detection pipeline.  
    threat_type = map_threat(event)  # Convert event patterns into a threat label.  
    risk_score = score_event(event, threat_type)  # Calculate a risk score.  
    vulnerability_reason = analyze_vulnerability(event, threat_type)  # Explain likely weakness.  
    is_suspicious = risk_score >= 50  # Treat score 50+ as suspicious.  
    next_action = "Review in dashboard and notify analyst." if is_suspicious else "Store for monitoring only."  # Choose next action.  

    return DetectionResult(  # Build the final detection result.  
        event_id=event.event_id,  # Keep original event id.  
        is_suspicious=is_suspicious,  # Save suspicious flag.  
        threat_type=threat_type,  # Save threat label.  
        risk_score=risk_score,  # Save score.  
        vulnerability_reason=vulnerability_reason,  # Save weakness explanation.  
        next_action=next_action,  # Save next action.  
    )  # Return the detection result.
