import json  # Convert Python objects into JSON text.  

from kafka import KafkaProducer  # Kafka producer client.  

from app.config import settings  # Read app settings.  


class EventProducer:  # Small wrapper around Kafka producer.  
    def __init__(self) -> None:  # Create the producer object.  
        self.producer = KafkaProducer(  # Build a Kafka producer instance.  
            bootstrap_servers=settings.kafka_bootstrap_servers,  # Tell it where Kafka is.  
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),  # Convert payload to bytes.  
        )  # Finish Kafka producer setup.  

    def send_event(self, payload: dict) -> None:  # Send one event to Kafka.  
        self.producer.send(settings.kafka_topic, payload)  # Publish the payload to the topic.  
        self.producer.flush()  # Flush immediately to keep the demo simple.
