import os
import logging
import warnings
import traceback
import json
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import uvicorn


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


warnings.filterwarnings("ignore", message="libuv only supports millisecond timer resolution")


from app.utils.zim_processor import process_medical_wikipedia
from app.models.drug_model import (
    Medicine, DrugInteraction, InteractionRequest, 
    InteractionResponse, MedicineSearchRequest, MedicineSearchResponse,
    MediGuideRequest
)
from app.services.data_loader import data_loader
from app.services.interaction_service import interaction_service
from app.models.llm_model import llm_model

app = FastAPI(
    title="Drug Interaction API",
    description="Offline API for drug interactions and medicine details",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the frontend directory
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        # Load data
        data_loader.load_data()
        
        # Initialize LLM with medicine names
        medicine_names = [med.name for med in data_loader.medicines]
        llm_model.load_model()
        llm_model.index_medicines(medicine_names)
        
        # Load medical knowledge base for solution-focused responses
        llm_model.load_medical_knowledge_base()
        
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise

@app.get("/")
async def root():
    return {"message": "Drug Interaction API is running"}

@app.get("/medicines", response_model=List[Medicine])
async def get_all_medicines(limit: int = Query(100, ge=1, le=1000)):
    """Get all medicines with optional limit"""
    return data_loader.medicines[:limit]

@app.post("/medicines/search", response_model=MedicineSearchResponse)
async def search_medicines(request: MedicineSearchRequest):
    """Search medicines by name or generic name"""
    results = data_loader.search_medicines(request.query, request.limit)
    return MedicineSearchResponse(
        medicines=results,
        total_count=len(results)
    )

@app.get("/medicines/{medicine_name}", response_model=Medicine)
async def get_medicine(medicine_name: str):
    """Get medicine details by name"""
    medicine = data_loader.get_medicine_by_name(medicine_name)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@app.post("/interactions/check", response_model=InteractionResponse)
async def check_interactions(request: InteractionRequest):
    """Check interactions between multiple medicines"""
    return interaction_service.check_interactions(request)

@app.get("/interactions/{drug_a}/{drug_b}", response_model=List[DrugInteraction])
async def get_interaction(drug_a: str, drug_b: str):
    """Get specific interaction between two drugs"""
    interactions = data_loader.find_interactions([drug_a, drug_b])
    if not interactions:
        raise HTTPException(status_code=404, detail="No interactions found")
    return interactions

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    wikipedia_data_exists = os.path.exists("app/data/wikipedia_en_medicine_mini_2025-08.zim")
    
    # Load medical chunks to check how many are available
    try:
        with open("app/data/medical_wikipedia_data/medical_chunks.json", 'r', encoding='utf-8') as f:
            medical_chunks = json.load(f)
        chunks_loaded = len(medical_chunks)
    except FileNotFoundError:
        chunks_loaded = 0
    
    return {
        "status": "healthy",
        "medicines_loaded": len(data_loader.medicines),
        "interactions_loaded": len(data_loader.drug_interactions),
        "model_loaded": llm_model.model is not None,
        "wikipedia_data_available": wikipedia_data_exists,
        "wikipedia_data_path": "app/data/wikipedia_en_medicine_mini_2025-08.zim",
        "wikipedia_chunks_loaded": chunks_loaded
    }


@app.post("/ask-mediguide")
async def ask_mediguide(request: MediGuideRequest = Body(...)):
    """Ask medical questions to MediGuide for solution-focused responses"""
    try:
        question = request.question

        # Generate solution-focused response using the medical knowledge base
        response = llm_model.generate_solution_response(question)

        return {
            "question": question,
            "response": response,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail="Error generating response")

@app.post("/process-wikipedia")
async def process_wikipedia_data():
    try:
        result = process_medical_wikipedia()
        return result
    except Exception as e:
        logger.error(f"Error processing Wikipedia data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
