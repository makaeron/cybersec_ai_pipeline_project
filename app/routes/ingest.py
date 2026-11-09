from fastapi import APIRouter  # Import API router.  

from app.models import SecurityEvent  # Import input model.  
from app.services.kafka_producer import EventProducer  # Import Kafka producer wrapper.  


router = APIRouter()  # Create router instance.  
producer = EventProducer()  # Create one producer object.  


@router.post("/events")  # Create an endpoint to receive one event.  
def create_event(event: SecurityEvent) -> dict:  # Receive and validate the event.  
    producer.send_event(event.model_dump(mode="json"))  # Send the event into Kafka.  
    return {"message": "Event accepted and sent to Kafka.", "event_id": event.event_id}  # Return confirmation.
