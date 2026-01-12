import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from pathlib import Path

from app.config import DRUG_INTERACTIONS_FILE, MEDICINE_DETAILS_FILE
from app.models.drug_model import Medicine, DrugInteraction

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        self.drug_interactions: List[DrugInteraction] = []
        self.medicines: List[Medicine] = []
        self.medicine_dict: Dict[str, Medicine] = {}
        self.interaction_dict: Dict[str, List[DrugInteraction]] = {}
        
    def load_data(self):
        """Load and parse both CSV files"""
        try:
            self._load_medicine_details()
            self._load_drug_interactions()
            self._build_indices()
            logger.info(f"Loaded {len(self.medicines)} medicines and {len(self.drug_interactions)} interactions")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def _load_medicine_details(self):
        """Load medicine details from CSV"""
        if MEDICINE_DETAILS_FILE.exists():
            df = pd.read_csv(MEDICINE_DETAILS_FILE)
            
            for index, row in df.iterrows():
                # Generate a unique medicine_id from the name if not provided
                medicine_id = str(row.get('medicine_id', ''))
                if not medicine_id:
                    # Create ID from medicine name by removing spaces and special chars
                    medicine_name = str(row.get('Medicine Name', '')).strip()
                    medicine_id = ''.join(c for c in medicine_name.lower() 
                                        if c.isalnum() or c.isspace()).replace(' ', '_')
                    # Add index to ensure uniqueness
                    medicine_id = f"{medicine_id}_{index}"
                
                medicine = Medicine(
                    medicine_id=medicine_id,
                    name=str(row.get('Medicine Name', '')).strip(),
                    generic_name=str(row.get('Composition', '')).strip(),
                    dosage_form="",  # Not available in the new CSV
                    strength="",     # Not available in the new CSV
                    manufacturer=str(row.get('Manufacturer', '')).strip(),
                    uses=str(row.get('Uses', '')).strip(),
                    side_effects=str(row.get('Side_effects', '')).strip(),
                    precautions=""   # Not available in the new CSV
                )
                self.medicines.append(medicine)
                logger.info(f"Loaded medicine: {medicine.name}")
    
    def _load_drug_interactions(self):
        """Load drug interactions from CSV"""
        if DRUG_INTERACTIONS_FILE.exists():
            df = pd.read_csv(DRUG_INTERACTIONS_FILE)
            
            for _, row in df.iterrows():
                interaction = DrugInteraction(
                    drug_a=str(row.get('Drug 1', '')),
                    drug_b=str(row.get('Drug 2', '')),
                    interaction_level="",  # Placeholder since not available in CSV
                    description=str(row.get('Interaction Description', '')),
                    severity="",  # Placeholder since not available in CSV
                    recommendations=None  # No recommendations available
                )
                self.drug_interactions.append(interaction)
    
    def _build_indices(self):
        """Build lookup indices for faster searching"""
        self.medicine_dict = {med.name.lower(): med for med in self.medicines}
        
        # Build interaction dictionary
        for interaction in self.drug_interactions:
            key = self._get_interaction_key(interaction.drug_a, interaction.drug_b)
            if key not in self.interaction_dict:
                self.interaction_dict[key] = []
            self.interaction_dict[key].append(interaction)
    
    def _get_interaction_key(self, drug_a: str, drug_b: str) -> str:
        """Create a consistent key for drug pairs (alphabetical order)"""
        drugs = [drug_a.lower(), drug_b.lower()]
        drugs.sort()
        return f"{drugs[0]}_{drugs[1]}"
    
    def find_interactions(self, medicine_names: List[str]) -> List[DrugInteraction]:
        """Find all interactions between the given medicines"""
        interactions = []
        checked_pairs = set()
        
        for i, med1 in enumerate(medicine_names):
            for j, med2 in enumerate(medicine_names):
                if i != j:
                    key = self._get_interaction_key(med1, med2)
                    if key not in checked_pairs and key in self.interaction_dict:
                        interactions.extend(self.interaction_dict[key])
                        checked_pairs.add(key)
        
        return interactions
    
    def search_medicines(self, query: str, limit: int = 10) -> List[Medicine]:
        """Search medicines by name or generic name"""
        query = query.lower()
        results = []
        
        for medicine in self.medicines:
            if (query in medicine.name.lower() or 
                (medicine.generic_name and query in medicine.generic_name.lower())):
                results.append(medicine)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_medicine_by_name(self, name: str) -> Optional[Medicine]:
        """Get medicine by exact name match"""
        return self.medicine_dict.get(name.lower())

# Global data loader instance
data_loader = DataLoader()