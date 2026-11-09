from langchain_core.prompts import ChatPromptTemplate  # Build simple prompts.  
from langchain_ollama import ChatOllama  # Connect LangChain to Ollama.  

from app.config import settings  # Read app settings.  
from app.models import DetectionResult, SecurityEvent, TriageResult  # Import typed models.  


class LLMTriageService:  # Wrap the LLM explanation logic.  
    def __init__(self) -> None:  # Build the prompt and model.  
        self.model = ChatOllama(model=settings.ollama_model, base_url=settings.ollama_base_url, temperature=0)  # Create chat model.  
        self.prompt = ChatPromptTemplate.from_template(  # Define one simple prompt template.  
            "You are a cybersecurity triage assistant. "  # Tell the model its role.  
            "Explain this incident in simple language. "  # Ask for simple language.  
            "Threat type: {threat_type}. "  # Insert detected threat.  
            "Risk score: {risk_score}. "  # Insert score.  
            "Message: {message}. "  # Insert original event message.  
            "Vulnerability reason: {vulnerability_reason}. "  # Insert likely weakness.  
            "Give a 3-part answer with summary, business impact, and operator action."  # Ask for fixed output.  
        )  # Finish prompt creation.  

    def triage(self, event: SecurityEvent, detection: DetectionResult) -> TriageResult:  # Send one incident to the LLM.  
        chain = self.prompt | self.model  # Create a simple LCEL chain.  
        response = chain.invoke(  # Run the prompt through the model.  
            {  # Pass all required prompt inputs.  
                "threat_type": detection.threat_type,  # Send threat type.  
                "risk_score": detection.risk_score,  # Send risk score.  
                "message": event.message,  # Send original message.  
                "vulnerability_reason": detection.vulnerability_reason,  # Send root cause.  
            }  # End input dictionary.  
        )  # Receive model response.  
        content = response.content if isinstance(response.content, str) else str(response.content)  # Convert content to text safely.  

        return TriageResult(  # Return a simple structured result.  
            event_id=event.event_id,  # Keep original event id.  
            summary=content,  # Store the generated summary text.  
            business_impact="Review possible user, system, or data exposure.",  # Keep business impact simple for now.  
            operator_action=detection.next_action,  # Reuse recommended operator action.  
        )  # Finish triage result.
