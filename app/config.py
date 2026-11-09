from pydantic_settings import BaseSettings  # Import settings base class.  


class Settings(BaseSettings):  # Create one place for environment-based settings.  
    app_name: str = "Cyber Security Threat Pipeline"  # Default app name.  
    api_host: str = "0.0.0.0"  # Default host for FastAPI.  
    api_port: int = 8000  # Default port for FastAPI.  
    kafka_bootstrap_servers: str = "localhost:9092"  # Kafka broker address.  
    kafka_topic: str = "security-events"  # Kafka topic for all security events.  
    redis_host: str = "localhost"  # Redis host.  
    redis_port: int = 6379  # Redis port.  
    opensearch_host: str = "localhost"  # OpenSearch host.  
    opensearch_port: int = 9200  # OpenSearch port.  
    opensearch_index: str = "security-events"  # OpenSearch index name.  
    ollama_base_url: str = "http://localhost:11434"  # Local Ollama endpoint.  
    ollama_model: str = "qwen3:8b"  # Default model name.  
    llm_rate_limit_per_minute: int = 20  # LLM call limit per minute.  

    class Config:  # Tell Pydantic where to read settings from.  
        env_file = ".env"  # Read from local .env if present.  
        env_file_encoding = "utf-8"  # Use UTF-8 for env values.  


settings = Settings()  # Create one reusable settings object.
