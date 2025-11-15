import streamlit as st
import groq  # latest Groq Python SDK

# --------------------- PAGE CONFIG ---------------------
st.set_page_config(
    page_title="Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------- GROQ CLIENT SETUP ---------------------
# Use your Groq API key here
GROQ_API_KEY = "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"

try:
    client = groq.Groq(api_key=GROQ_API_KEY)  # ✅ Correct way
    st.sidebar.success("✅ Groq API Connected Successfully")
except Exception as e:
    st.sidebar.error(f"❌ Failed to initialize Groq client: {e}")
    st.stop()

# --------------------- PERSONAL ASSISTANT CLASS ---------------------
class PersonalAssistant:
    def __init__(self):
        self.conversation_history = []
        self.system_prompt = (
            "You are a helpful, friendly, and professional personal assistant. "
            "Your capabilities include:\n"
            "- Answering general knowledge questions\n"
            "- Helping with writing and editing\n"
            "- Providing explanations on various topics\n"
            "- Offering suggestions and recommendations\n"
            "- Assisting with problem-solving\n"
            "Always be polite, concise, and helpful. If you don't know something, be honest about it."
        )

    def get_response(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history[-6:])

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            assistant_message = response.choices[0].message.content
        except Exception as e:
            assistant_message = f"⚠️ An error occurred: {e}"

        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def clear_history(self):
        self.conversation_history = []

# --------------------- STREAMLIT APP ---------------------
def main():
    if "assistant" not in st.session_state:
        st.session_state.assistant = PersonalAssistant()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar
    with st.sidebar:
        st.title("🤖 Personal Assistant")
        st.markdown("---")
        st.subheader("About")
        st.write("Your AI-powered personal assistant (powered by Groq).")
        st.markdown("---")
        st.subheader("Settings")
        if st.button("🔄 Clear Conversation", use_container_width=True):
            st.session_state.assistant.clear_history()
            st.session_state.messages = []
            st.experimental_rerun()
        st.markdown("---")
        st.caption("Model: llama-3.1-8b-instant")

    # Chat area
    st.title("💬 Chat with Your Assistant")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.assistant.get_response(prompt)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Quick actions
    st.markdown("---")
    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    quick_actions = {
        "💡 Brainstorm Ideas": "Help me brainstorm some creative ideas for a project",
        "📝 Writing Help": "Help me improve my writing skills and give me tips",
        "🔍 Explain Concept": "Explain machine learning in simple terms",
        "🎯 Daily Tips": "Give me some productivity tips for today"
    }
    for col, (btn, text) in zip([col1, col2, col3, col4], quick_actions.items()):
        with col:
            if st.button(btn, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": text})
                with st.chat_message("user"):
                    st.markdown(text)
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        resp = st.session_state.assistant.get_response(text)
                        st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})

if __name__ == "__main__":
    main()


   
    


          
    
   
