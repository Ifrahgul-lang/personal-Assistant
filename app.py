# Create enhanced app.py with all fixes
%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import requests
import os
import re
import base64
from typing import List, Dict, Any
import time

# Try to import Groq, but provide fallback
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# ==================== ENHANCED CONFIGURATION ====================

st.set_page_config(
    page_title="AI Health Assistant Pro 🏥",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS WITH FALLBACKS ====================

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
    }
    .emergency-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
        border: 3px solid #ff4757;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: none;
    }
    .symptom-item {
        background: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .risk-high { 
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white; 
        padding: 0.5rem 1rem; 
        border-radius: 5px; 
        font-weight: bold;
    }
    .risk-medium { 
        background: linear-gradient(135deg, #ffa726 0%, #f57c00 100%);
        color: white; 
        padding: 0.5rem 1rem; 
        border-radius: 5px; 
        font-weight: bold;
    }
    .risk-low { 
        background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
        color: white; 
        padding: 0.5rem 1rem; 
        border-radius: 5px; 
        font-weight: bold;
    }
    .chat-user { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem; 
        margin: 0.5rem 0; 
        border-radius: 15px 15px 0 15px; 
        max-width: 80%;
        margin-left: auto;
    }
    .chat-assistant { 
        background: #f5f5f5;
        color: #333;
        padding: 1rem; 
        margin: 0.5rem 0; 
        border-radius: 15px 15px 15px 0; 
        max-width: 80%;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== GROQ AI CLIENT WITH FALLBACK ====================

class GroqHealthAssistant:
    def __init__(self):
        self.api_key = os.getenv('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')
        self.client = None
        self.available = False
        
        if GROQ_AVAILABLE and self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                self.available = True
            except Exception as e:
                st.sidebar.warning(f"Groq API Error: {e}")
        else:
            if not GROQ_AVAILABLE:
                st.sidebar.info("ℹ️ Groq library not installed. Using enhanced rule-based system.")
            elif not self.api_key:
                st.sidebar.info("ℹ️ GROQ_API_KEY not found. Using enhanced rule-based system.")
    
    def analyze_with_groq(self, prompt: str, context: Dict = None) -> str:
        """Analyze health queries using Groq's powerful AI"""
        if not self.available or not self.client:
            return self._fallback_response(prompt, context)
        
        try:
            system_prompt = """You are an advanced AI health assistant. Provide accurate, helpful, and safe medical information.
            
            GUIDELINES:
            - Always emphasize this is not a substitute for professional medical advice
            - For emergencies, immediately direct users to seek professional help
            - Provide clear, evidence-based information
            - Be empathetic and understanding
            - Suggest following up with healthcare providers
            - Use simple language that's easy to understand
            - Include practical recommendations when appropriate"""
            
            full_prompt = f"Context: {context}\n\nUser Query: {prompt}"
            
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=1024
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return self._fallback_response(prompt, context)
    
    def _fallback_response(self, prompt: str, context: Dict = None) -> str:
        """Enhanced fallback response system"""
        prompt_lower = prompt.lower()
        
        # Emergency detection
        emergency_keywords = ['chest pain', 'heart attack', 'can\'t breathe', 'stroke', 'unconscious']
        if any(keyword in prompt_lower for keyword in emergency_keywords):
            return "🚨 **EMERGENCY SITUATION DETECTED**\n\n**IMMEDIATE ACTION REQUIRED:**\n1. Call Emergency Services (911) immediately\n2. Do not delay seeking professional medical care\n3. Have someone stay with you until help arrives"
        
        # Symptom-specific responses
        if 'headache' in prompt_lower:
            return """**Headache Analysis** 🤕

**Common Causes:** Tension, migraine, dehydration, sinus issues

**Recommendations:**
• Rest in a quiet, dark room
• Stay well hydrated
• Use over-the-counter pain relief as directed
• Apply cold compress to forehead

**Seek medical care for:**
- Severe, sudden headache
- Headache with fever or confusion
- Headache after head injury"""

        elif 'fever' in prompt_lower:
            return """**Fever Management** 🌡️

**Recommended Actions:**
• Monitor temperature regularly
• Stay hydrated with water and electrolyte solutions
• Use fever-reducing medication as directed
• Rest and avoid strenuous activities

**Seek Medical Care if:**
- Fever above 103°F (39.4°C)
- Fever lasts more than 3 days
- Accompanied by severe symptoms"""

        elif 'cough' in prompt_lower:
            return """**Cough Relief** 🤧

**Comfort Measures:**
• Use humidifier or steam inhalation
• Stay hydrated to thin mucus
• Use cough drops or lozenges
• Avoid irritants like smoke

**Consult Healthcare Provider if:**
- Cough persists beyond 2 weeks
- Difficulty breathing
- Coughing up blood"""

        else:
            return """**Health Guidance** 🏥

Thank you for sharing your health concerns. Based on your description, I recommend:

**General Advice:**
• Monitor your symptoms closely
• Stay hydrated and get adequate rest
• Practice good hygiene

**When to Seek Professional Care:**
• Symptoms worsen or don't improve
• New concerning symptoms develop

**Remember:** This is for informational purposes only. Always consult healthcare professionals for medical advice."""

# ==================== ENHANCED HEALTH ANALYSIS ENGINE ====================

class AdvancedHealthAnalyzer:
    def __init__(self):
        self.symptom_database = self._load_enhanced_symptom_database()
        self.emergency_conditions = self._load_emergency_conditions()
        
    def _load_enhanced_symptom_database(self) -> Dict:
        return {
            "Respiratory": ["cough", "shortness of breath", "chest pain", "wheezing", "congestion", "sore throat"],
            "Cardiovascular": ["chest pain", "palpitations", "dizziness", "swelling", "irregular heartbeat"],
            "Neurological": ["headache", "dizziness", "numbness", "vision changes", "confusion", "seizure"],
            "Digestive": ["nausea", "vomiting", "diarrhea", "constipation", "abdominal pain", "bloating"],
            "Musculoskeletal": ["joint pain", "back pain", "muscle ache", "stiffness", "swelling"],
            "General": ["fever", "fatigue", "weakness", "weight loss", "chills", "sweating"]
        }
    
    def _load_emergency_conditions(self) -> Dict:
        return {
            "heart_attack": {
                "symptoms": ["chest pain", "shortness of breath", "pain in arms", "nausea", "cold sweat"],
                "response": "🚨 CALL EMERGENCY SERVICES IMMEDIATELY - Possible heart attack"
            },
            "stroke": {
                "symptoms": ["face drooping", "arm weakness", "speech difficulty", "confusion"],
                "response": "🚨 CALL EMERGENCY SERVICES IMMEDIATELY - Possible stroke"
            },
            "severe_allergy": {
                "symptoms": ["difficulty breathing", "swelling face", "swelling throat", "hives", "dizziness"],
                "response": "🚨 CALL EMERGENCY SERVICES - Severe allergic reaction"
            }
        }

    def analyze_symptoms(self, text: str, user_context: Dict = None) -> Dict[str, Any]:
        """Enhanced symptom analysis"""
        analysis = {
            "symptoms_found": [],
            "categories": [],
            "severity_score": 0,
            "risk_level": "low",
            "is_emergency": False,
            "emergency_type": None,
            "confidence": 0.0,
            "recommendations": [],
            "follow_up_questions": [],
            "suggested_actions": []
        }
        
        if not text:
            return analysis
        
        text_lower = text.lower()
        
        # Extract symptoms
        symptoms_found = []
        severity_indicators = 0
        
        for category, symptoms in self.symptom_database.items():
            for symptom in symptoms:
                if symptom in text_lower:
                    symptoms_found.append(symptom)
                    if category not in analysis["categories"]:
                        analysis["categories"].append(category)
                    # Count severity indicators
                    if any(word in text_lower for word in ["severe", "intense", "unbearable", "worst"]):
                        severity_indicators += 1
        
        analysis["symptoms_found"] = symptoms_found
        analysis["severity_score"] = min(severity_indicators * 0.5, 3.0)
        
        # Check for emergency conditions
        for condition, data in self.emergency_conditions.items():
            emergency_symptoms = [s for s in data["symptoms"] if s in text_lower]
            if len(emergency_symptoms) >= 2:
                analysis["is_emergency"] = True
                analysis["emergency_type"] = condition
                analysis["risk_level"] = "high"
                break
        
        # Calculate risk level
        if analysis["is_emergency"]:
            analysis["risk_level"] = "high"
        elif len(symptoms_found) >= 3 or analysis["severity_score"] >= 2.0:
            analysis["risk_level"] = "medium"
        else:
            analysis["risk_level"] = "low"
        
        # Confidence calculation
        analysis["confidence"] = min(len(symptoms_found) * 0.2 + analysis["severity_score"] * 0.1, 0.9)
        
        # Generate recommendations
        analysis.update(self._generate_recommendations(analysis))
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict) -> Dict:
        """Generate comprehensive recommendations"""
        recommendations = {
            "recommendations": [],
            "suggested_actions": [],
            "follow_up_questions": []
        }
        
        # Emergency recommendations
        if analysis["is_emergency"]:
            emergency_response = self.emergency_conditions[analysis["emergency_type"]]["response"]
            recommendations["recommendations"].extend([
                emergency_response,
                "Do not drive yourself to the hospital",
                "Have someone stay with you until help arrives"
            ])
        
        # Risk-based recommendations
        if analysis["risk_level"] == "high":
            recommendations["recommendations"].extend([
                "Contact healthcare provider within 24 hours",
                "Monitor symptoms closely for changes",
                "Avoid strenuous activities"
            ])
        elif analysis["risk_level"] == "medium":
            recommendations["recommendations"].extend([
                "Schedule appointment with healthcare provider",
                "Rest and maintain hydration",
                "Monitor symptoms for improvement or worsening"
            ])
        else:
            recommendations["recommendations"].extend([
                "Self-monitor for 24-48 hours",
                "Practice general wellness habits",
                "Seek care if symptoms persist or worsen"
            ])
        
        # Symptom-specific advice
        if any(symptom in analysis["symptoms_found"] for symptom in ["fever", "chills"]):
            recommendations["suggested_actions"].extend([
                "Monitor temperature every 4-6 hours",
                "Stay hydrated with water and electrolyte solutions",
                "Use fever-reducing medication as directed"
            ])
        
        if any(symptom in analysis["symptoms_found"] for symptom in ["cough", "congestion"]):
            recommendations["suggested_actions"].extend([
                "Use humidifier or steam inhalation",
                "Stay hydrated to thin mucus",
                "Avoid irritants like smoke and strong odors"
            ])
        
        # Follow-up questions
        recommendations["follow_up_questions"] = [
            "How long have you been experiencing these symptoms?",
            "Have you noticed any triggers or patterns?",
            "Are you currently taking any medications?",
            "Do you have any known medical conditions?",
            "Have you traveled recently or been around sick individuals?"
        ]
        
        return recommendations

# ==================== ENHANCED MULTILINGUAL SUPPORT ====================

class AdvancedMultilingualSupport:
    def __init__(self):
        self.supported_languages = {
            "English": "en",
            "Urdu": "ur", 
            "Hindi": "hi",
            "Arabic": "ar",
            "Spanish": "es"
        }
        
        self.health_phrases = self._load_health_phrases()
    
    def _load_health_phrases(self) -> Dict:
        return {
            "emergency": {
                "en": "🚨 EMERGENCY - SEEK IMMEDIATE MEDICAL ATTENTION",
                "ur": "🚨 ایمرجنسی - فوری طبی امداد حاصل کریں",
                "hi": "🚨 आपातकाल - तत्काल चिकित्सा सहायता लें",
                "es": "🚨 EMERGENCIA - BUSQUE ATENCIÓN MÉDICA INMEDIATA"
            },
            "welcome": {
                "en": "Welcome to AI Health Assistant Pro 🏥",
                "ur": "AI ہیلتھ اسسٹنٹ پرو میں خوش آمدید 🏥",
                "hi": "AI हेल्थ असिस्टेंट प्रो में आपका स्वागत है 🏥",
                "es": "Bienvenido a AI Health Assistant Pro 🏥"
            }
        }
    
    def get_phrase(self, key: str, language: str = "en") -> str:
        """Get translated phrase"""
        lang_code = self.supported_languages.get(language, "en")
        return self.health_phrases.get(key, {}).get(lang_code, self.health_phrases.get(key, {}).get("en", key))

# ==================== HEALTH DATA MANAGER ====================

class HealthDataManager:
    def __init__(self):
        self.user_profile = {}
        self.health_history = []
    
    def save_health_record(self, symptoms: str, analysis: Dict):
        """Save health analysis record"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "symptoms": symptoms,
            "analysis": analysis,
            "risk_level": analysis.get("risk_level", "unknown"),
            "is_emergency": analysis.get("is_emergency", False)
        }
        self.health_history.append(record)
        
        # Keep only last 50 records
        if len(self.health_history) > 50:
            self.health_history = self.health_history[-50:]
    
    def get_health_insights(self) -> Dict:
        """Generate health insights from history"""
        if not self.health_history:
            return {}
        
        insights = {
            "total_analyses": len(self.health_history),
            "emergency_cases": sum(1 for r in self.health_history if r["is_emergency"]),
            "common_categories": {},
            "recent_activity": len([r for r in self.health_history if datetime.fromisoformat(r["timestamp"]) > datetime.now() - timedelta(days=7)])
        }
        
        # Analyze common categories
        for record in self.health_history:
            for category in record["analysis"].get("categories", []):
                insights["common_categories"][category] = insights["common_categories"].get(category, 0) + 1
        
        return insights

# ==================== MAIN APPLICATION ====================

def main():
    # Initialize services with error handling
    try:
        groq_assistant = GroqHealthAssistant()
        health_analyzer = AdvancedHealthAnalyzer()
        multilingual = AdvancedMultilingualSupport()
        data_manager = HealthDataManager()
    except Exception as e:
        st.error(f"Initialization Error: {e}")
        return
    
    # Initialize session state with defaults
    default_states = {
        "messages": [],
        "analysis_history": [],
        "user_language": "English",
        "current_tab": "Dashboard",
        "user_profile": {
            "age_group": "",
            "existing_conditions": [],
            "medications": [],
            "allergies": []
        }
    }
    
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Enhanced sidebar with error handling
    try:
        with st.sidebar:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 15px; color: white; margin-bottom: 2rem;'>
                <h2>🏥 AI Health Assistant Pro</h2>
                <p>Advanced Healthcare Companion</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Language selection
            st.subheader("🌐 Language Settings")
            selected_language = st.selectbox(
                "Choose Language",
                options=list(multilingual.supported_languages.keys()),
                key="language_selector",
                index=0
            )
            st.session_state.user_language = selected_language
            
            # User Profile
            st.markdown("---")
            st.subheader("👤 User Profile")
            
            with st.expander("Update Health Profile", expanded=False):
                age_group = st.selectbox(
                    "Age Group",
                    ["Select", "Under 18", "18-30", "31-50", "51-65", "65+"],
                    key="profile_age"
                )
                
                conditions = st.multiselect(
                    "Existing Conditions",
                    ["None", "Hypertension", "Diabetes", "Heart Disease", "Asthma", "Arthritis", "Other"],
                    key="profile_conditions"
                )
                
                medications = st.text_input("Current Medications", placeholder="List medications separated by commas")
                allergies = st.text_input("Allergies", placeholder="List allergies separated by commas")
                
                if st.button("💾 Save Profile"):
                    st.session_state.user_profile.update({
                        "age_group": age_group,
                        "existing_conditions": conditions,
                        "medications": [m.strip() for m in medications.split(",") if m.strip()],
                        "allergies": [a.strip() for a in allergies.split(",") if a.strip()]
                    })
                    st.success("Profile updated!")
            
            # Navigation
            st.markdown("---")
            st.subheader("🧭 Navigation")
            
            tabs = {
                "🏠 Dashboard": "Dashboard",
                "💬 Health Chat": "Health Chat", 
                "🔍 Symptom Analysis": "Symptom Analysis",
                "📊 Health Analytics": "Analytics",
                "🆘 Emergency Guide": "Emergency",
                "🌐 Multi-language": "Multilingual"
            }
            
            for tab_name, tab_value in tabs.items():
                if st.button(tab_name, use_container_width=True, key=f"btn_{tab_value}"):
                    st.session_state.current_tab = tab_value
                    st.rerun()
            
            # Quick stats
            st.markdown("---")
            st.subheader("📈 Quick Stats")
            insights = data_manager.get_health_insights()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Analyses", insights.get("total_analyses", 0))
            with col2:
                st.metric("Emergency Cases", insights.get("emergency_cases", 0))
            
            # Emergency quick access
            st.markdown("---")
            if st.button("🚨 EMERGENCY GUIDE", use_container_width=True, type="secondary"):
                st.session_state.current_tab = "Emergency"
                st.rerun()
                
    except Exception as e:
        st.sidebar.error(f"Sidebar Error: {e}")
    
    # Main content router with error handling
    try:
        current_tab = st.session_state.current_tab
        
        if current_tab == "Dashboard":
            show_dashboard(health_analyzer, multilingual, data_manager, groq_assistant)
        elif current_tab == "Health Chat":
            show_health_chat(groq_assistant, health_analyzer, multilingual, data_manager)
        elif current_tab == "Symptom Analysis":
            show_symptom_analysis(health_analyzer, multilingual, data_manager, groq_assistant)
        elif current_tab == "Analytics":
            show_analytics(data_manager)
        elif current_tab == "Emergency":
            show_emergency_guide(multilingual)
        elif current_tab == "Multilingual":
            show_multilingual_support(multilingual)
            
    except Exception as e:
        st.error(f"Application Error: {e}")
        st.info("Please refresh the page and try again.")

def show_dashboard(analyzer, multilingual, data_manager, groq_assistant):
    """Enhanced dashboard"""
    st.markdown('<div class="main-header">🏥 AI Health Assistant Pro</div>', unsafe_allow_html=True)
    
    # Welcome message
    welcome_msg = multilingual.get_phrase("welcome", st.session_state.user_language)
    st.success(f"**{welcome_msg}** • Language: {st.session_state.user_language}")
    
    if groq_assistant.available:
        st.info("🤖 **Groq AI Enabled** - Real-time intelligent health analysis")
    else:
        st.info("ℹ️ **Enhanced Rule-Based System** - Comprehensive health guidance")
    
    # Hero section with metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 AI Powered</h3>
            <p>Advanced Health Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🌐 Multi-language</h3>
            <p>5 Languages Supported</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🚨 Emergency</h3>
            <p>Instant Detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Analytics</h3>
            <p>Health Insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(3)
    
    with action_cols[0]:
        if st.button("💬 Start Health Chat", use_container_width=True):
            st.session_state.current_tab = "Health Chat"
            st.rerun()
    
    with action_cols[1]:
        if st.button("🔍 Symptom Analysis", use_container_width=True):
            st.session_state.current_tab = "Symptom Analysis"
            st.rerun()
    
    with action_cols[2]:
        if st.button("🆘 Emergency Guide", use_container_width=True):
            st.session_state.current_tab = "Emergency"
            st.rerun()
    
    # Feature highlights
    st.markdown("---")
    st.subheader("🚀 Advanced Features")
    
    features = [
        {"icon": "🤖", "title": "AI-Powered Analysis", "desc": "Intelligent symptom recognition"},
        {"icon": "🌐", "title": "Multi-language Support", "desc": "5 languages including Urdu, Hindi"},
        {"icon": "🚨", "title": "Emergency Detection", "desc": "Critical condition identification"},
        {"icon": "📊", "title": "Health Analytics", "desc": "Comprehensive health tracking"},
        {"icon": "💊", "title": "Medication Database", "desc": "Treatment information"},
        {"icon": "🔍", "title": "Smart Recommendations", "desc": "Personalized health advice"}
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{feature['icon']} {feature['title']}</h3>
                <p>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_health_chat(groq_assistant, analyzer, multilingual, data_manager):
    """AI-powered health chat"""
    st.header("💬 AI Health Assistant Chat")
    
    st.info("💡 Describe your symptoms in detail for accurate analysis. Remember: informational purposes only.")
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-user"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-assistant"><strong>Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Describe your health concerns...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate AI response
        with st.spinner("🤔 Analyzing..."):
            # Perform symptom analysis
            analysis = analyzer.analyze_symptoms(user_input, st.session_state.user_profile)
            
            # Prepare context for AI
            context = {
                "symptoms": user_input,
                "risk_level": analysis.get("risk_level", "unknown"),
                "is_emergency": analysis.get("is_emergency", False),
                "user_profile": st.session_state.user_profile
            }
            
            # Get AI response
            ai_response = groq_assistant.analyze_with_groq(user_input, context)
            
            # Add emergency alert if needed
            if analysis.get('is_emergency'):
                emergency_msg = multilingual.get_phrase("emergency", st.session_state.user_language)
                final_response = f"🚨 **{emergency_msg}**\n\n{ai_response}"
            else:
                final_response = ai_response
            
            # Add assistant response
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            
            # Store analysis
            data_manager.save_health_record(user_input, analysis)
            
            st.rerun()

def show_symptom_analysis(analyzer, multilingual, data_manager, groq_assistant):
    """Enhanced symptom analysis"""
    st.header("🔍 Symptom Analysis")
    
    with st.form("symptom_analysis"):
        st.subheader("Describe Your Symptoms")
        
        symptoms_text = st.text_area(
            "Please describe your symptoms in detail:",
            placeholder="Example: I've been having headaches and fatigue for 3 days...",
            height=120
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.selectbox("Duration", ["Select", "Less than 24 hours", "1-3 days", "3-7 days", "1-2 weeks", "More than 2 weeks"])
            severity = st.select_slider("Severity", options=["Mild", "Moderate", "Severe"], value="Moderate")
        
        with col2:
            onset = st.selectbox("Onset", ["Select", "Sudden", "Gradual"])
            impact = st.selectbox("Impact", ["Select", "No impact", "Mild impact", "Moderate impact", "Severe impact"])
        
        if st.form_submit_button("🚀 Analyze Symptoms"):
            if symptoms_text:
                with st.spinner("🔍 Analyzing symptoms..."):
                    analysis = analyzer.analyze_symptoms(symptoms_text, st.session_state.user_profile)
                    
                    # Store analysis
                    data_manager.save_health_record(symptoms_text, analysis)
                    
                    # Display results
                    display_analysis_results(analysis, multilingual)
            else:
                st.warning("Please describe your symptoms.")

def display_analysis_results(analysis: Dict, multilingual):
    """Display analysis results"""
    st.success("✅ Analysis Complete!")
    
    if analysis["is_emergency"]:
        emergency_msg = multilingual.get_phrase("emergency", st.session_state.user_language)
        st.markdown(f'<div class="emergency-alert">{emergency_msg}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Analysis Summary")
        
        risk_level = analysis["risk_level"]
        risk_class = f"risk-{risk_level}"
        st.markdown(f"**Risk Level:** <span class='{risk_class}'>{risk_level.upper()}</span>", unsafe_allow_html=True)
        
        st.metric("Symptoms Found", len(analysis["symptoms_found"]))
        st.metric("Confidence", f"{analysis['confidence']:.0%}")
        
        st.write("**Identified Symptoms:**")
        for symptom in analysis["symptoms_found"]:
            st.markdown(f'<div class="symptom-item">• {symptom.title()}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 Assessment")
        
        st.write("**Affected Systems:**")
        for category in analysis["categories"]:
            st.write(f"• {category}")
        
        if analysis["is_emergency"]:
            st.error(f"**Emergency Type:** {analysis['emergency_type'].replace('_', ' ').title()}")
    
    # Recommendations
    st.subheader("💡 Recommendations")
    for i, recommendation in enumerate(analysis["recommendations"][:3], 1):
        st.write(f"{i}. {recommendation}")
    
    if analysis["suggested_actions"]:
        st.subheader("⚡ Suggested Actions")
        for action in analysis["suggested_actions"][:3]:
            st.write(f"• {action}")

def show_analytics(data_manager):
    """Health analytics dashboard"""
    st.header("📊 Health Analytics")
    
    insights = data_manager.get_health_insights()
    
    if not insights or insights["total_analyses"] == 0:
        st.info("No health data available yet. Start by analyzing some symptoms!")
        return
    
    # Key metrics
    st.subheader("📈 Health Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Analyses", insights["total_analyses"])
    with col2:
        st.metric("Emergency Cases", insights["emergency_cases"])
    with col3:
        st.metric("Recent Activity", insights["recent_activity"])
    
    # Sample charts
    st.subheader("📊 Health Trends")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    health_data = pd.DataFrame({
        'date': dates,
        'symptom_score': np.random.normal(3, 1, 30) + np.sin(np.arange(30) * 0.3) * 2,
        'wellness_score': 10 - (np.random.normal(3, 1, 30) + np.sin(np.arange(30) * 0.3) * 2)
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_symptoms = px.line(health_data, x='date', y='symptom_score', title='Symptom Severity Trend')
        st.plotly_chart(fig_symptoms, use_container_width=True)
    
    with col2:
        fig_wellness = px.area(health_data, x='date', y='wellness_score', title='Wellness Score Trend')
        st.plotly_chart(fig_wellness, use_container_width=True)
    
    # Analysis history
    st.subheader("📝 Recent Analyses")
    if data_manager.health_history:
        history_df = pd.DataFrame([
            {
                'Date': datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d %H:%M'),
                'Symptoms': item['symptoms'][:50] + '...' if len(item['symptoms']) > 50 else item['symptoms'],
                'Risk Level': item['risk_level'].title()
            }
            for item in data_manager.health_history[-5:]
        ])
        st.dataframe(history_df, use_container_width=True, hide_index=True)

def show_emergency_guide(multilingual):
    """Emergency preparedness guide"""
    st.header("🆘 Emergency Guide")
    
    emergency_msg = multilingual.get_phrase("emergency", st.session_state.user_language)
    st.markdown(f'<div class="emergency-alert">{emergency_msg}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚑 Emergency Protocols")
        
        emergencies = {
            "Heart Attack": {
                "symptoms": ["Chest pain", "Shortness of breath", "Pain in arms", "Nausea", "Cold sweat"],
                "actions": ["Call 911 immediately", "Chew aspirin if available", "Stay calm and rest"]
            },
            "Stroke (FAST)": {
                "symptoms": ["Face drooping", "Arm weakness", "Speech difficulty"],
                "actions": ["Call 911 immediately", "Note time symptoms started", "Do NOT give food/drink"]
            },
            "Severe Allergy": {
                "symptoms": ["Difficulty breathing", "Swelling face/throat", "Hives", "Dizziness"],
                "actions": ["Use epinephrine if available", "Call 911", "Lie down with feet elevated"]
            }
        }
        
        for condition, info in emergencies.items():
            with st.expander(condition):
                st.write("**Symptoms:**")
                for symptom in info["symptoms"]:
                    st.write(f"• {symptom}")
                st.write("**Actions:**")
                for action in info["actions"]:
                    st.write(f"• {action}")
    
    with col2:
        st.subheader("📞 Emergency Contacts")
        
        contacts = {
            "Emergency Services": "911",
            "Poison Control": "1-800-222-1222",
            "Mental Health Crisis": "988"
        }
        
        for service, number in contacts.items():
            st.write(f"**{service}:** `{number}`")
        
        st.subheader("🏠 Emergency Kit")
        kit_items = ["Bandages", "Gauze", "Antiseptic", "Thermometer", "Pain relievers", "Emergency blanket"]
        for item in kit_items:
            st.write(f"☐ {item}")

def show_multilingual_support(multilingual):
    """Multi-language support"""
    st.header("🌐 Multi-language Support")
    
    st.success(f"**Current Language:** {st.session_state.user_language}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗣️ Health Phrases")
        
        phrases = {
            "English": {
                "I need help": "I need medical assistance",
                "Where is hospital?": "Can you direct me to the nearest hospital?",
                "I have pain": "I'm experiencing pain and need help"
            },
            "Urdu": {
                "I need help": "مجھے طبی امداد کی ضرورت ہے",
                "Where is hospital?": "آپ مجھے قریبی ہسپتال کا راستہ بتا سکتے ہیں؟",
                "I have pain": "مجھے درد ہو رہا ہے اور مدد کی ضرورت ہے"
            },
            "Hindi": {
                "I need help": "मुझे चिकित्सा सहायता की आवश्यकता है",
                "Where is hospital?": "क्या आप मुझे निकटतम अस्पताल का रास्ता बता सकते हैं?",
                "I have pain": "मुझे दर्द हो रहा है और मदद की जरूरत है"
            }
        }
        
        if st.session_state.user_language in phrases:
            phrases_df = pd.DataFrame([
                {"English": eng, st.session_state.user_language: trans}
                for eng, trans in phrases[st.session_state.user_language].items()
            ])
            st.dataframe(phrases_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🎯 Language Tips")
        
        if st.session_state.user_language == "Urdu":
            st.write("""
            **Urdu Health Terms:**
            - درد (Dard) - Pain
            - بخار (Bukhaar) - Fever  
            - کھانسی (Khansi) - Cough
            - متلی (Matli) - Nausea
            """)
        elif st.session_state.user_language == "Hindi":
            st.write("""
            **Hindi Health Terms:**
            - दर्द (Dard) - Pain
            - बुखार (Bukhaar) - Fever
            - खांसी (Khaansi) - Cough
            - जी मिचलाना (Ji michlana) - Nausea
            """)
        else:
            st.write("""
            **Communication Tips:**
            - Speak slowly and clearly
            - Use simple words
            - Point to body parts if needed
            - Keep emergency phrases saved
            """)

if __name__ == "__main__":
    main()
    


          
    
   
