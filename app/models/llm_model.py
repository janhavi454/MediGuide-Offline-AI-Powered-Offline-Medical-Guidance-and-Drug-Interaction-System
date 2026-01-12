import json
import os
from typing import List, Dict
import logging
import litellm  

logger = logging.getLogger(__name__)

class LLMModel:
    def __init__(self):
        self.model = None
        self.use_llm = False 
        self.wikipedia_data = None

    def load_model(self):
        """Load the actual LLM model if available, otherwise use local mode"""
        try:
           
            self.model = "gpt-3.5-turbo" 
            self.use_llm = True
            logger.info("Real LLM model configured")
        except Exception as e:
            self.use_llm = False
            logger.warning(f"Using local response mode: {e}")

    def index_medicines(self, medicine_names: List[str]):
        """Index medicine names for better search"""
        print(f"Indexing medicines: {medicine_names}")

    def generate_response(self, question: str) -> str:
        """Generate response using either real LLM or local responses"""
        try:
            if self.use_llm and self.model:
                # Use real LLM API
                messages = [
                    {
                        "role": "user",
                        "content": question  # Text only, no images
                    }
                ]
                
                response = litellm.completion(
                    model=self.model,  # Use the configured working model
                    messages=messages,
                    max_tokens=500
                )
                
                return response.choices[0].message.content
            else:
                # Fall back to local responses
                return self._get_local_response(question)
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_local_response(question)

    def _get_local_response(self, question: str) -> str:
        """Local response fallback"""
        responses = {
            "What are the side effects of aspirin?": "Common side effects include nausea, vomiting, and stomach pain.",
            "What should I do if I have a fever?": "Stay hydrated, rest, and consider taking fever-reducing medication.",
            "Can I take ibuprofen with aspirin?": "It's generally not recommended to take them together without consulting a doctor."
        }
        return responses.get(question, "I'm sorry, I don't have an answer for that. Please try a different question.")

    def load_medical_knowledge_base(self):
        """Load comprehensive medical knowledge base for solutions and recommendations"""
        try:
            self.medical_knowledge = {
                # Common conditions and their treatments
                "fever": {
                    "symptoms": ["fever", "high temperature", "body heat"],
                    "tablets": ["Paracetamol 500mg", "Acetaminophen 500mg", "Ibuprofen 400mg (if no stomach issues)"],
                    "dosage": "Take 1-2 tablets every 6-8 hours as needed. Do not exceed 8 tablets in 24 hours.",
                    "emergency": "Seek immediate medical attention if temperature exceeds 103°F (39.4°C) or lasts more than 3 days",
                    "care": ["Rest and stay hydrated", "Use light clothing and bedding", "Take lukewarm baths", "Monitor temperature regularly"]
                },
                "headache": {
                    "symptoms": ["headache", "head pain", "migraine", "tension headache"],
                    "tablets": ["Paracetamol 500mg", "Ibuprofen 400mg", "Aspirin 300mg (adults only)"],
                    "dosage": "Take 1-2 tablets every 6-8 hours as needed.",
                    "emergency": "Seek immediate medical attention if headache is sudden and severe, or accompanied by confusion, seizures, or vision changes",
                    "care": ["Rest in a quiet, dark room", "Apply cold or warm compress", "Stay hydrated", "Practice relaxation techniques"]
                },
                "cold": {
                    "symptoms": ["cold", "runny nose", "sore throat", "cough", "congestion"],
                    "tablets": ["Paracetamol 500mg (for pain/fever)", "Decongestant tablets", "Cough suppressants if needed"],
                    "dosage": "Follow package instructions. Paracetamol: 1-2 tablets every 6-8 hours.",
                    "emergency": "Seek medical attention if symptoms worsen or last more than 10 days, or if you have difficulty breathing",
                    "care": ["Rest and stay hydrated", "Use saline nasal sprays", "Gargle with warm salt water", "Use humidifier"]
                },
                "stomach pain": {
                    "symptoms": ["stomach pain", "abdominal pain", "stomach ache", "belly pain"],
                    "tablets": ["Antacid tablets (for acidity)", "Buscopan 10mg (for cramps)", "Paracetamol 500mg (for pain)"],
                    "dosage": "Antacid: 1-2 tablets as needed. Buscopan: 1 tablet 3 times daily.",
                    "emergency": "Seek immediate medical attention if pain is severe, persistent, or accompanied by vomiting blood, black stools, or high fever",
                    "care": ["Avoid spicy and fatty foods", "Eat smaller, frequent meals", "Stay hydrated", "Apply warm compress"]
                },
                "allergy": {
                    "symptoms": ["allergy", "allergic reaction", "itching", "rash", "hives"],
                    "tablets": ["Cetirizine 10mg", "Loratadine 10mg", "Fexofenadine 180mg"],
                    "dosage": "Take 1 tablet once daily.",
                    "emergency": "Seek immediate medical attention if you experience difficulty breathing, swelling of face/throat, or dizziness",
                    "care": ["Avoid known allergens", "Use air purifiers", "Keep windows closed during high pollen seasons"]
                },
                "emergency": {
                    "symptoms": ["emergency", "chest pain", "heart attack", "stroke", "severe injury", "unconscious"],
                    "actions": [
                        "Call emergency services immediately (911 or local emergency number)",
                        "For chest pain: Chew 1 aspirin 300mg tablet (if not allergic)",
                        "For stroke: Remember FAST (Face drooping, Arm weakness, Speech difficulty, Time to call emergency)",
                        "Do not give food or drink to unconscious person",
                        "Perform CPR if trained and person is not breathing",
                        "Stay with the person until help arrives"
                    ]
                }
            }
            logger.info("Medical knowledge base loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading medical knowledge base: {e}")
            return False

    def generate_solution_response(self, question: str) -> str:
        """Generate solution-focused response with specific tablet recommendations and emergency guidance"""
        if not hasattr(self, 'medical_knowledge') or not self.medical_knowledge:
            return "Medical knowledge base is not loaded. Please restart the application."

        question_lower = question.lower()

        # Check for emergency situations first
        if any(word in question_lower for word in self.medical_knowledge["emergency"]["symptoms"]):
            return self._format_emergency_response()

        # Find relevant conditions based on symptoms mentioned in the question
        relevant_conditions = []
        for condition, data in self.medical_knowledge.items():
            if condition != "emergency":  # Skip emergency as it's handled separately
                for symptom in data["symptoms"]:
                    if symptom in question_lower:
                        relevant_conditions.append((condition, data))
                        break

        if relevant_conditions:
            # Return the most relevant condition's solution
            best_condition, best_data = relevant_conditions[0]
            return self._format_solution_response(best_condition, best_data)

        # If no specific condition found, provide general guidance
        return self._get_general_guidance(question)

    def _format_solution_response(self, condition: str, data: dict) -> str:
        """Format a comprehensive solution response"""
        response = f"**SOLUTION FOR {condition.upper()}**\n\n"

        response += "💊 **RECOMMENDED TABLETS:**\n"
        for tablet in data["tablets"]:
            response += f"• {tablet}\n"
        response += f"\n📋 **DOSAGE:** {data['dosage']}\n\n"

        response += "⚠️ **WHEN TO SEEK MEDICAL HELP:**\n"
        response += f"• {data['emergency']}\n\n"

        response += "🏠 **HOME CARE INSTRUCTIONS:**\n"
        for care_item in data["care"]:
            response += f"• {care_item}\n"

        response += f"\n\n⚠️ **IMPORTANT:** This is general guidance only. Always consult with a healthcare professional for personalized medical advice."

        return response

    def _format_emergency_response(self) -> str:
        """Format emergency response with immediate actions"""
        response = "**🚨 MEDICAL EMERGENCY - ACT IMMEDIATELY 🚨**\n\n"

        response += "📞 **IMMEDIATE ACTIONS REQUIRED:**\n"
        for action in self.medical_knowledge["emergency"]["actions"]:
            response += f"• {action}\n"

        response += "\n\n**DO NOT DELAY - CALL FOR HELP NOW!**"
        response += "\n\n⚠️ **This is a medical emergency. Professional medical care is required immediately.**"

        return response

    def _get_general_guidance(self, question: str) -> str:
        """Provide general guidance when specific condition is not identified"""
        return f"I understand you're asking about: '{question}'\n\nFor personalized medical advice, please consult with a healthcare professional. They can provide specific recommendations based on your individual health situation.\n\nIf you're experiencing concerning symptoms, please seek medical attention promptly."

# Global instance
llm_model = LLMModel()
