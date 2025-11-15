import streamlit as st
import groq
import os

# --------------------- PAGE CONFIG ---------------------
st.set_page_config(
    page_title="Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------- GROQ API SETUP ---------------------
GROQ_API_KEY = "gsk_4pz0G8cY9iV0fVw2h8K3WGdyb3FYhVfHh8a3w0TQY1qL1jXQ1aK"

try:
    client = groq.Client(api_key=GROQ_API_KEY)
    st.sidebar.success("✅ Groq API Connected Successfully")
except Exception as e:
    st.error(f"❌ Failed to initialize Groq client: {e}")
    st.stop()

# --------------------- PERSONAL ASSISTANT CLASS ---------------------
class PersonalAssistant:
    def __init__(self):
        self.conversation_history = []
        self.setup_assistant_personality()
    
    def setup_assistant_personality(self):
        """Define the assistant's personality and capabilities"""
        self.system_prompt = """You are a helpful, friendly, and professional personal assistant. 
        Your capabilities include:
        - Answering general knowledge questions
        - Helping with writing and editing
        - Providing explanations on various topics
        - Offering suggestions and recommendations
        - Assisting with problem-solving
        - Being conversational and engaging
        
        Always be polite, concise, and helpful. If you don't know something, be honest about it."""
    
    def get_response(self, user_input):
        """Get response from Groq API"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Prepare messages for API call
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history[-6:])  # Keep last 6 messages for context
            
            # Call Groq API
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message["content"]
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            return f"⚠️ An error occurred: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

# --------------------- STREAMLIT APP ---------------------
def main():
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = PersonalAssistant()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # --------------------- SIDEBAR ---------------------
    with st.sidebar:
        st.title("🤖 Personal Assistant")
        st.markdown("---")
        
        st.subheader("About")
        st.write("Your AI-powered personal assistant powered by Groq's fast LLMs!")
        
        st.markdown("---")
        st.subheader("Capabilities")
        st.write("""
        - 💬 General conversations
        - 📚 Knowledge & explanations
        - ✍️ Writing assistance
        - 🔍 Problem solving
        - 💡 Suggestions & ideas
        """)
        
        st.markdown("---")
        st.subheader("Settings")
        if st.button("🔄 Clear Conversation", use_container_width=True):
            st.session_state.assistant.clear_history()
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.caption("Powered by Groq LLaMA 3.1 8B Instant")
    
    # --------------------- MAIN CHAT AREA ---------------------
    st.title("💬 Personal Assistant")
    st.markdown("Hello! I'm your personal assistant powered by Groq's AI models. How can I help you today?")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.assistant.get_response(prompt)
                st.markdown(response)
        
        # Add assistant response to messages
        st.session_state.messages.append({"role": "assistant", "content": response})

    # --------------------- QUICK ACTIONS ---------------------
    st.markdown("---")
    st.subheader("Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    quick_actions = {
        "💡 Brainstorm Ideas": "Help me brainstorm some creative ideas for a project",
        "📝 Writing Help": "Help me improve my writing skills and give me tips",
        "🔍 Explain Concept": "Explain machine learning in simple terms",
        "🎯 Daily Tips": "Give me some productivity tips for today"
    }
    
    for col, (button_text, prompt_text) in zip([col1, col2, col3, col4], quick_actions.items()):
        with col:
            if st.button(button_text, use_container_width=True):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt_text})
                with st.chat_message("user"):
                    st.markdown(prompt_text)
                
                # Get and display response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = st.session_state.assistant.get_response(prompt_text)
                        st.markdown(response)
                
                # Add assistant response
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
