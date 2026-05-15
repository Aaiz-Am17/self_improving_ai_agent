import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Industrial AutoML", page_icon="🏭", layout="wide")
st.title("🏭 Industrial AI MLOps Agent")

# =====================================================
# SESSION STATE (MEMORY)
# =====================================================
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "needs_approval" not in st.session_state:
    st.session_state.needs_approval = False

if "pending_plan" not in st.session_state:
    st.session_state.pending_plan = {}

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.header("⚙️ Configuration")
    dataset_path = st.text_input("Dataset Path", value="data/datasets/titanic.csv")
    st.caption(f"Session ID: `{st.session_state.thread_id}`")

# =====================================================
# CHAT INTERFACE
# =====================================================
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Only show chat input if we are NOT waiting for an approval
if not st.session_state.needs_approval:
    if prompt := st.chat_input("Enter instructions (e.g., 'Analyze this dataset')..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Agent is orchestrating workflow..."):
            payload = {
                "thread_id": st.session_state.thread_id,
                "message": prompt,
                "dataset_path": dataset_path
            }
            
            res = requests.post(f"{API_URL}/chat", json=payload)
            data = res.json()
            
            # Check if the graph hit the breakpoint
            if data.get("needs_approval"):
                st.session_state.needs_approval = True
                plan = data["response"].get("preprocessing_plan", {})
                st.session_state.pending_plan = plan
                st.rerun() # Refresh to show buttons
            else:
                answer = "Workflow Complete!\n\n"
                answer += f"🎯 **Accuracy:** `{data['response'].get('model_accuracy', 'N/A')}`"
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.chat_message("assistant").write(answer)

# =====================================================
# HUMAN-IN-THE-LOOP UI
# =====================================================
if st.session_state.needs_approval:
    st.warning("⚠️ **Human Approval Required**")
    st.write("The Pipeline Architect has proposed the following preprocessing plan:")
    st.json(st.session_state.pending_plan)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Approve Plan", use_container_width=True):
            with st.spinner("Executing Pipeline..."):
                payload = {
                    "thread_id": st.session_state.thread_id,
                    "dataset_path": dataset_path,
                    "approval_decision": "1"
                }
                res = requests.post(f"{API_URL}/chat", json=payload)
                
                # Check if the backend accepted the request
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.needs_approval = False
                    
                    answer = "Plan Approved. Model Execution Complete!\n\n"
                    answer += f"🎯 **Final Accuracy:** `{data['response'].get('model_accuracy', 'N/A')}`"
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
                else:
                    st.error(f"Backend Error: {res.text}")

    with col2:
        if st.button("❌ Reject Plan", type="primary", use_container_width=True):
            payload = {
                "thread_id": st.session_state.thread_id,
                "dataset_path": dataset_path,
                "approval_decision": "2"
            }
            requests.post(f"{API_URL}/chat", json=payload)
            st.session_state.needs_approval = False
            
            st.session_state.messages.append({"role": "assistant", "content": "Plan Rejected. Execution stopped."})
            st.rerun()