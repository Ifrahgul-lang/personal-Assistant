import streamlit as st
import openai
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
api_key = os.getenv('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')
if not api_key:
    st.error("OpenAI API key not found in environment variables!")
else:
    client = openai.OpenAI(api_key=api_key)

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
        """Get response from OpenAI API"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Prepare messages for API call
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history[-6:])  # Keep last 6 messages for context
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except openai.AuthenticationError:
            return "❌ Authentication Error: Please check if your API key is valid and active."
        except openai.RateLimitError:
            return "⏰ Rate Limit Exceeded: Please wait a moment before sending another message."
        except openai.APIError as e:
            return f"🔧 API Error: {str(e)}"
        except Exception as e:
            return f"⚠️ An unexpected error occurred: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

def main():
    # Check if API key is available
    if not api_key:
        st.error("""
        ❌ OpenAI API key not found!
        
        Please make sure you have:
        1. Created a `.env` file in the same directory
        2. Added your API key to the `.env` file like this:
           OPENAI_API_KEY=your_actual_api_key_here
        
        Get your API key from: https://platform.openai.com/account/api-keys
        """)
        return
    
    # Test API connection
    try:
        # Simple test to verify the API key works
        models = client.models.list()
        api_status = "✅ API Connected Successfully"
    except openai.AuthenticationError:
        st.error("""
        ❌ Invalid API Key!
        
        Please check:
        1. Your API key is correct and active
        2. You have sufficient credits in your OpenAI account
        3. The API key is properly set in the .env file
        
        Get a new API key from: https://platform.openai.com/account/api-keys
        """)
        return
    except Exception as e:
        st.error(f"❌ API Connection Error: {str(e)}")
        return

    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = PersonalAssistant()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 Personal Assistant")
        st.markdown("---")
        
        st.subheader("About")
        st.write("Your AI-powered personal assistant ready to help with various tasks!")
        
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
        if st.button("🔄 Clear Conversation", use_container_width=True):
            st.session_state.assistant.clear_history()
            st.session_state.messages = []
            st.rerun()
        
        # API status
        st.markdown("---")
        st.success(api_status)
        st.caption("Powered by OpenAI GPT-3.5 Turbo")
    
    # Main content area
    st.title("💬 Personal Assistant")
    st.markdown("Hello! I'm your personal assistant. How can I help you today?")
    
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

    # Quick action buttons
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
                # Add to chat directly
                if prompt := st.chat_input("Type your message here..."):
                    pass  # This is just to avoid the placeholder issue
                st.session_state.messages.append({"role": "user", "content": prompt_text})
                with st.chat_message("user"):
                    st.markdown(prompt_text)
                
                # Get and display response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = st.session_state.assistant.get_response(prompt_text)
                        st.markdown(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

if __name__ == "__main__":
    main()
