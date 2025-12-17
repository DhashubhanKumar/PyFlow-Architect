import streamlit as st
import uuid
from main import app

st.set_page_config(page_title="Python DevTeam", page_icon="🐍", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

with st.sidebar:
    st.header("Settings")
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

st.title("🐍 Autonomous Python Developer")

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask for any Python task...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Thoughts are HIDDEN by default as requested
        thought_container = st.expander("🔍 View Agent Thinking Process", expanded=False)
        
        with st.status("🚀 Coding and Testing...", expanded=True) as status:
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            inputs = {"messages": [user_input], "attempts": 0, "is_fixed": False}
            
            for output in app.stream(inputs, config=config):
                for node_name, state_update in output.items():
                    thought_container.subheader(f"Agent: {node_name.upper()}")
                    
                    if "messages" in state_update:
                        thought_container.info(state_update["messages"][-1])
                    
                    if "current_code" in state_update:
                        thought_container.code(state_update["current_code"], language="python")

            status.update(label="✅ Python Verified!", state="complete", expanded=False)

        # Show final result
        full_state = app.get_state(config).values
        st.divider()
        st.subheader("Final Verified Python Code")
        st.code(full_state["current_code"], language="python")
        
        if full_state["is_fixed"]:
            st.success(f"Verified in {full_state['attempts']} attempt(s)!")
        else:
            st.error("Could not fully verify code within 3 attempts.")
            
        st.session_state.messages.append({"role": "assistant", "content": "Code generated and tested."})