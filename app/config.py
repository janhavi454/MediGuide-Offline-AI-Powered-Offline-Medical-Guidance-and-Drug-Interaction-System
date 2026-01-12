import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# File paths
DRUG_INTERACTIONS_FILE = DATA_DIR / "db_drug_interactions.csv"
MEDICINE_DETAILS_FILE = DATA_DIR / "Medicine_Details.csv"

# Model settings
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
SIMILARITY_THRESHOLD = 0.7