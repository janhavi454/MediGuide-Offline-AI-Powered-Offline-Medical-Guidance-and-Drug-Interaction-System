from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Medicine(BaseModel):
    medicine_id: str
    name: str
    generic_name: Optional[str] = None
    dosage_form: Optional[str] = None
    strength: Optional[str] = None
    manufacturer: Optional[str] = None
    uses: Optional[str] = None
    side_effects: Optional[str] = None
    precautions: Optional[str] = None

class DrugInteraction(BaseModel):
    drug_a: str
    drug_b: str
    interaction_level: str
    description: str
    severity: str
    recommendations: Optional[str] = None

class InteractionRequest(BaseModel):
    medicines: List[str]
    patient_info: Optional[Dict[str, Any]] = None

class InteractionResponse(BaseModel):
    interactions: List[DrugInteraction]
    severity_summary: Dict[str, int]
    recommendations: List[str]

class MedicineSearchRequest(BaseModel):
    query: str
    limit: int = 10

class MedicineSearchResponse(BaseModel):
    medicines: List[Medicine]
    total_count: int

class MediGuideRequest(BaseModel):
    question: str
