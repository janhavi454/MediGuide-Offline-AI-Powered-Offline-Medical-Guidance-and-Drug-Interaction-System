import sys
sys.path.append("F:\\offline_llm")  

from app.models.drug_model import InteractionRequest, InteractionResponse, DrugInteraction



from typing import List, Dict, Any
import logging

from app.models.drug_model import InteractionRequest, InteractionResponse, DrugInteraction
from app.services.data_loader import data_loader

logger = logging.getLogger(__name__)

class InteractionService:
    def __init__(self):
        self.data_loader = data_loader
    
    def check_interactions(self, request: InteractionRequest) -> InteractionResponse:
        """Check interactions between multiple medicines"""
        interactions = self.data_loader.find_interactions(request.medicines)
        
        # Calculate severity summary
        severity_summary = {
            "high": 0,
            "moderate": 0,
            "low": 0,
            "unknown": 0
        }
        
        for interaction in interactions:
            severity = interaction.severity.lower() if interaction.severity else "unknown"
            severity_summary[severity] = severity_summary.get(severity, 0) + 1
        
        # Generate recommendations
        recommendations = self._generate_recommendations(interactions, severity_summary)
        
        return InteractionResponse(
            interactions=interactions,
            severity_summary=severity_summary,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, interactions: List[DrugInteraction], 
                                severity_summary: Dict[str, int]) -> List[str]:
        """Generate recommendations based on interactions"""
        recommendations = []
        
        if severity_summary["high"] > 0:
            recommendations.append("⚠️ HIGH RISK: Consult your doctor immediately before taking these medications together.")
        
        if severity_summary["moderate"] > 0:
            recommendations.append("⚠️ MODERATE RISK: Monitor closely and consult your doctor about these combinations.")
        
       
        for interaction in interactions:
            if interaction.recommendations and interaction.recommendations.strip():
                rec = f"For {interaction.drug_a} + {interaction.drug_b}: {interaction.recommendations}"
                recommendations.append(rec)
        
        if not recommendations:
            recommendations.append("No significant interactions found. Always follow your doctor's advice.")
        
        return recommendations
   
interaction_service = InteractionService()
    
