import streamlit as st
import time
import Utils.status_manager as status_manager
from langgraph_agent import run_workflow
from langgraph_agent import resume_workflow
from Memory.store import store
import asyncio

# ----------------- StatusBox -----------------
class StatusBox:
    def __init__(self):
        self.container = st.empty()
        self.lines = [""]  # single line for rotating messages

    def add_line(self, initial_message=""):
        self.lines[0] = initial_message
        self._refresh()
        return 0  # always line 0

    def update_line(self, line_idx, new_message):
        self.lines[0] = new_message 
        self._refresh()

    def _refresh(self):
        html = f"<div style='font-size:14px; line-height:1.3; color:gray; margin:0;'>{self.lines[0]}</div>"
        self.container.markdown(html, unsafe_allow_html=True)

# ----------------- Initialize Session State -----------------
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False
if 'user_choice' not in st.session_state:
    st.session_state.user_choice = None
if 'current_query' not in st.session_state:
    st.session_state.current_query = None
if 'interrupt_message' not in st.session_state:
    st.session_state.interrupt_message = ""
if 'waiting_for_resume' not in st.session_state:
    st.session_state.waiting_for_resume = False

# ----------------- Popup Dialog Function -----------------
@st.dialog("Confirmation Required")
def show_confirmation_popup():
    st.write(st.session_state.interrupt_message)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Yes", key="yes_btn", type="primary", use_container_width=True):
            st.session_state.user_choice = True  # Boolean True for Yes
            st.session_state.show_popup = False
            st.session_state.waiting_for_resume = True
            st.rerun()
    
    with col2:
        if st.button("No", key="no_btn", use_container_width=True):
            st.session_state.user_choice = False  # Boolean False for No
            st.session_state.show_popup = False
            st.session_state.waiting_for_resume = True
            st.rerun()

# ----------------- Handle Popup Display -----------------
if st.session_state.show_popup:
    show_confirmation_popup()

# ----------------- App Title -----------------
st.title("Curb")

# ----------------- Sidebar Registration -----------------
with st.sidebar:
    st.header("User Details")

    if "registered" not in st.session_state:
        st.session_state.registered = False

    if not st.session_state.registered:
        name = st.text_input("Name")
        email = st.text_input("Email")
        if st.button("Save"):
            if name and email:
                
                store.put(("user_123", 'credentials'), "123", {
                "name": name,
                "email": email,
                })
                
                store.put(("user_123", "memories"), "123", {'text': f'Name: {name}, Email : {email}'})
                
                st.session_state.registered = True
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.success(f"Welcome {name}!")
                st.rerun()  # refresh to hide inputs 
            else:
                st.error("Please fill in both fields")
    else:
        st.success(f"Registered as {st.session_state.user_name} ({st.session_state.user_email})")
        if st.button("Logout"):
            st.session_state.registered = False
            st.rerun()

# ----------------- Chat UI -----------------
if st.session_state.get("registered", False):

    # Initialize session state for storing chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = [] 

    # Display all chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle resume workflow after user makes choice
    if st.session_state.waiting_for_resume and st.session_state.user_choice is not None:
        with st.chat_message("assistant"):
            status_box = StatusBox()
            
            with st.spinner("Processing your response...", show_time=True):
                print(f"Resuming workflow with query: {st.session_state.current_query}")
                print(f"User choice (hitl_response): {st.session_state.user_choice}")
                
                # Call resume_workflow with original query and boolean choice
                ai_response = asyncio.run(resume_workflow(
                    st.session_state.current_query, 
                    st.session_state.user_choice
                ))
                
                print('Final ai_response: ', ai_response)
                
                # Display status updates
                updates = status_manager.get_status()
                for update in updates:
                    status_box.update_line(0, update)
                    time.sleep(1)
                
                status_box.update_line(0, "")
                
                # Display final AI response
                st.markdown(ai_response)
                
                # Save AI response in chat history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Reset all states
        st.session_state.waiting_for_resume = False
        st.session_state.user_choice = None
        st.session_state.current_query = None
        st.session_state.interrupt_message = ""
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        status_manager.clear_status()
        
        # Add and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            status_box = StatusBox()
            
            # Run initial workflow
            with st.spinner("Creating Response", show_time=True):
                print(f"Running workflow with prompt: {prompt}")
                ai_response = asyncio.run(run_workflow(prompt))
                print('Initial ai_response: ', ai_response)
                
                # Check if response contains interrupt
                if "__interrupt__" in ai_response:
                    print('Interrupt detected - showing popup')
                    
                    # Extract interrupt information
                    interrupt_payload = ai_response["__interrupt__"][0].value
                    interrupt_prompt = interrupt_payload.get("prompt", "Do you want to proceed?")
                    
                    # Store current query and interrupt message for resume
                    st.session_state.current_query = prompt
                    st.session_state.interrupt_message = interrupt_prompt
                    
                    # Show popup
                    st.session_state.show_popup = True
                    st.session_state.user_choice = None
                    
                    # Display interrupt message in chat
                    st.write("⚠️ **Action requires confirmation:**")
                    st.write(interrupt_prompt)
                    st.info("Please respond using the confirmation dialog.")
                    
                    # Trigger rerun to show popup
                    st.rerun()
                
                else:
                    # Normal response - no interrupt
                    print('Normal response - no interrupt')
                    
                    # Display status updates
                    updates = status_manager.get_status()
                    for update in updates:
                        status_box.update_line(0, update)
                        time.sleep(1)
                    
                    status_box.update_line(0, "")
                    
                    # Display final AI response
                    st.markdown(ai_response)
                    
                    # Save AI response in chat history
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})