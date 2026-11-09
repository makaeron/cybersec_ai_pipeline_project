from app.models import SecurityEvent  # Import the input event model.  


def map_threat(event: SecurityEvent) -> str:  # Map raw event patterns to threat labels.  
    message_text = event.message.lower()  # Lowercase the message for simple matching.  
    event_type = event.event_type.lower()  # Lowercase the event type too.  

    if "ignore previous instructions" in message_text or "reveal secrets" in message_text:  # Look for prompt injection text.  
        return "Prompt Injection"  # Return threat label.  
    if "or '1'='1" in message_text or "union select" in message_text:  # Look for simple SQL injection patterns.  
        return "SQL Injection"  # Return threat label.  
    if "<script>" in message_text:  # Look for simple XSS pattern.  
        return "Cross-Site Scripting"  # Return threat label.  
    if "failed_login" in event_type or "failed login" in message_text:  # Look for repeated login failure events.  
        return "Brute Force Attempt"  # Return threat label.  
    return "General Suspicious Activity"  # Use a safe default label.
