from pydantic import BaseModel, Field, validator
from typing import List

class PredictionRequest(BaseModel):
    features: List[float] = Field(..., example=[5.1, 3.5, 1.4, 0.2])

    @validator('features')
    def validate_features(cls, v):
        if len(v) != 4:
            raise ValueError('Exactly 4 features required: sepal_length, sepal_width, petal_length, petal_width')
        
        feature_names = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
        for i, (val, name) in enumerate(zip(v, feature_names)):
            if val < 0:
                raise ValueError(f'{name} cannot be negative (got {val})')
        
        # Reject all-zero inputs — biologically impossible for a real flower
        if all(val == 0 for val in v):
            raise ValueError('All feature values are zero. Please enter valid iris measurements.')
        
        # At minimum, sepal length and petal length should be > 0 for a real flower
        if v[0] <= 0 or v[2] <= 0:
            raise ValueError('Sepal Length and Petal Length must be greater than 0 for a valid iris measurement.')
        
        return v

class PredictionResponse(BaseModel):
    prediction: int
    prediction_name: str
