import json  # Parse Kafka message bytes into Python objects.  

from kafka import KafkaConsumer  # Kafka consumer client.  

from app.config import settings  # Read app settings.  
from app.models import SecurityEvent  # Import typed event model.  
from app.services.detection_engine import detect_event  # Import detection logic.  
from app.services.llm_triage import LLMTriageService  # Import LLM triage helper.  
from app.services.opensearch_service import OpenSearchService  # Import OpenSearch helper.  
from app.services.redis_state import RedisState  # Import Redis helper.  


def main() -> None:  # Start the consumer loop.  
    consumer = KafkaConsumer(  # Build a Kafka consumer.  
        settings.kafka_topic,  # Subscribe to the security topic.  
        bootstrap_servers=settings.kafka_bootstrap_servers,  # Tell consumer where Kafka lives.  
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),  # Decode JSON bytes into dicts.  
        auto_offset_reset="earliest",  # Read from earliest in local demos.  
        enable_auto_commit=True,  # Keep commit handling simple.  
        group_id="security-consumer-group",  # Give the consumer group a name.  
    )  # Finish Kafka consumer setup.  

    redis_state = RedisState()  # Create Redis helper object.  
    search_service = OpenSearchService()  # Create OpenSearch helper object.  
    llm_service = LLMTriageService()  # Create LLM helper object.  

    for message in consumer:  # Read messages forever.  
        event = SecurityEvent(**message.value)  # Validate Kafka payload against the event model.  

        if redis_state.seen_event(event.event_id):  # Skip duplicate events.  
            continue  # Move to the next event.  

        detection = detect_event(event)  # Run detection logic.  
        triage = None  # Prepare triage variable.  

        if detection.is_suspicious and redis_state.allow_llm_call():  # Only call the LLM for suspicious events and within rate limits.  
            triage = llm_service.triage(event, detection)  # Generate human-readable triage.  

        document = {  # Build one searchable document.  
            "event": event.model_dump(mode="json"),  # Save the original event.  
            "detection": detection.model_dump(),  # Save detection results.  
            "triage": triage.model_dump() if triage else None,  # Save triage if available.  
        }  # Finish searchable document.  

        search_service.index_document(document_id=event.event_id, body=document)  # Store event in OpenSearch.  
        print(f"Processed event: {event.event_id}")  # Print a simple local log line.  


if __name__ == "__main__":  # Only run main when script is executed directly.  
    main()  # Start the consumer loop.
