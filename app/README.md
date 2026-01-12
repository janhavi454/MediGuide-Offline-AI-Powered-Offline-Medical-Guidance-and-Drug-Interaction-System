# MediGuide Offline: AI-Powered Offline Medical Guidance and Drug Interaction System
# At point 5 specify the command how to run backened
## Project Overview
The MediGuide Offline: AI-Powered Offline Medical Guidance and Drug Interaction System is an offline, fast, and efficient RESTful web service designed to provide comprehensive drug interaction checks and detailed medicine information. It integrates domain-specific data with advanced language model capabilities to offer solution-focused medical advice and interactions assessment. The API is built with FastAPI and serves a static frontend for user interaction.

## Features
- Search medicines by name or composition.
- Retrieve detailed medicine information including uses, side effects, and manufacturer.
- Check potential interactions between multiple medicines.
- Retrieve detailed interaction descriptions and severity.
- AI-powered medical question answering with solution-focused guidance.
- Offline usage with local datasets and fallback responses.
- Health endpoint to monitor data loading and service status.
- Serve static frontend assets.

### Prerequisites
- Python 3.10 or above
- pip package manager

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Set up a virtual environment :
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place the data files in the `app/data/` directory:
   - `db_drug_interactions.csv`: Contains drug interaction records.
   - `Medicine_Details.csv`: Detailed medicine descriptions.
   - `wikipedia_en_medicine_mini_2025-08.zim`: Medical knowledge base.
   - JSON chunk files for Wikipedia data under `app/data/medical_wikipedia_data/`.

5. Run the API server:
   ```bash
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   ```

## API Endpoints

- `GET /`  
  Health check, returns service running status.

- `GET /medicines?limit={int}`  
  Retrieves a list of medicines, optionally limited in number (default 100).

- `POST /medicines/search`  
  Search medicines by name or composition. Request body:
  ```json
  {
    "query": "aspirin",
    "limit": 10
  }
  ```

- `GET /medicines/{medicine_name}`  
  Fetch detailed information for a specific medicine.

- `POST /interactions/check`  
  Checks interactions between multiple medicines. Request body:
  ```json
  {
    "medicines": ["aspirin", "ibuprofen"],
    "patient_info": {}
  }
  ```

- `GET /interactions/{drug_a}/{drug_b}`  
  Get interactions between two specific drugs.

- `POST /ask-mediguide`  
  Ask medical questions with AI-powered solution-focused responses. Request body:
  ```json
  {
    "question": "What are the side effects of aspirin?"
  }
  ```

- `POST /process-wikipedia`  
  Trigger reprocessing of the medical Wikipedia data.

- `GET /health`  
  Returns detailed statistics about data loaded and system health.

## Data Sources
- **Drug Interactions CSV**: Contains pairs of interacting drugs and their descriptions.
- **Medicine Details CSV**: Includes medicine names, composition, manufacturer info, uses, and side effects.
- **Medical Wikipedia ZIM file**: A snapshot of English Wikipedia medical content used for advanced AI knowledge base.

## AI and Language Model
The API integrates an LLM (GPT-3.5-turbo by default) to provide natural language medical guidance and answers. It also includes a fallback local mode to respond with canned answers when LLM is not available. The AI model:

- Loads medicine names for efficient indexing.
- Accesses a preprocessed medical knowledge base for solution-focused responses.
- Handles emergency and common conditions with tablet recommendations, dosages, and home care instructions.

## Project Structure

```
app/
├── main.py               # FastAPI app and endpoints
├── config.py             # Configuration and constants
├── models/               # Pydantic models for API data validation
│   ├── drug_model.py
│   └── llm_model.py
├── services/             # Business logic services
│   ├── data_loader.py    # Data loading and indexing
│   └── interaction_service.py  # Drug interaction checking logic
├── utils/                # Utility modules
├── data/                 # Data files (CSV, JSON, ZIM)
├── requirements.txt      # Python dependencies
frontend/                 # Frontend UI assets
README.md                 # This file
```

## Dependencies
- FastAPI==0.104.1
- Uvicorn==0.24.0
- Pandas==2.1.3
- Sentence-transformers==2.2.2
- Transformers==4.35.2
- Torch==2.1.1
- Numpy==1.24.3
- python-multipart==0.0.6