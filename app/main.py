from fastapi import FastAPI  # Import FastAPI.  

from app.config import settings  # Import settings.  
from app.routes.ingest import router as ingest_router  # Import event router.  


app = FastAPI(title=settings.app_name)  # Create the FastAPI application.  

app.include_router(ingest_router, prefix="/api", tags=["ingestion"])  # Register ingestion routes.  


@app.get("/health")  # Create a simple health endpoint.  
def health() -> dict:  # Return current health state.  
    return {"status": "ok", "app": settings.app_name}  # Return health data.

class EvaluationScore(BaseModel):
    factual_accuracy: int       # 1-5: does explanation reference real data?
    evidence_sufficiency: int   # 1-5: does conclusion match evidence?
    mitre_correctness: int      # 1-5: is MITRE tactic/technique accurate?
    action_specificity: int     # 1-5: are recommendations concrete?
    confidence_calibration: int # 1-5: appropriate uncertainty expressed?
    evaluator_notes: str        # what was wrong or right
    verdict: str                # "supported" | "unsupported" | "partial"

@app.post("/alerts/{alert_id}/evaluate", tags=["Evaluation"])
async def evaluate_alert(
    alert_id: str,
    score: EvaluationScore,
    opensearch: OpenSearchClient = Depends(get_opensearch)
):
    """Score an AI-generated alert triage explanation on 5 dimensions."""
    existing = opensearch.get_document(settings.opensearch_index_alerts, alert_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Alert not found")

    updated = {
        **existing,
        "evaluation": score.model_dump(),
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "overall_score": sum([
            score.factual_accuracy,
            score.evidence_sufficiency,
            score.mitre_correctness,
            score.action_specificity,
            score.confidence_calibration
        ]) / 5
    }
    opensearch.index_document(settings.opensearch_index_alerts, alert_id, updated)
    return {"alert_id": alert_id, "overall_score": updated["overall_score"]}
