import joblib
import os
from fastapi import APIRouter, Depends, HTTPException
from backend.api.models import PredictionRequest, PredictionResponse
from backend.core.auth import get_api_key
from backend.core.logging import logger

router = APIRouter()

# Load model at startup
try:
    model_path = os.path.join(os.path.dirname(__file__), '../../ml_model/model.pkl')
    # Use fallback paths to avoid breaking
    if not os.path.exists(model_path):
        model_path = os.path.abspath(os.path.join(os.getcwd(), 'ml_model', 'model.pkl'))
        
    model_data = joblib.load(model_path)
    model = model_data['model']
    target_names = model_data['target_names']
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None
    target_names = []

@router.post("/predict", response_model=PredictionResponse, dependencies=[Depends(get_api_key)])
async def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    try:
        # Fail-safe check: Reject all-zero inputs even if validator was bypassed
        if all(v == 0 for v in request.features):
            raise HTTPException(status_code=400, detail="Invalid input: All measurements are zero. Please enter valid flower data.")

        # Request features as list for sklearn
        input_data = [request.features]
        pred = model.predict(input_data)[0]
        pred_name = target_names[pred]
        
        logger.info(f"Prediction made: class={pred}, name={pred_name}")
        return PredictionResponse(prediction=int(pred), prediction_name=pred_name)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
