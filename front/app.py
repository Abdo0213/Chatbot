import streamlit as st
import requests

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered") 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

st.markdown(""" 
    <style>
        body {
            background: linear-gradient(135deg, #121212 0%, #1a1a2e 100%);
            color: white;
        }
        
        .message {
            display: flex;  
            gap: 10px;  
            align-items: center; 
            margin-bottom: 15px;
        }  
        
        .user-message-container {
            display: flex; 
            justify-content: flex-end; 
            width: 100%; 
        }
        
        .user-bubble {  
            display: flex;
            background: linear-gradient(135deg, #4a90e2 0%, #3a7bd5 100%); 
            color: white;  
            padding: 12px 16px;  
            border-radius: 18px 18px 0 18px;  
            max-width: 75%;  
            margin: 5px 0;  
            order: 1;
            box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
            transition: all 0.3s ease;
        }  
        
        .bot-bubble {  
            display: flex;
            background: linear-gradient(135deg, #f5f5dc 0%, #e8e8d8 100%);
            color: #333;  
            padding: 12px 16px;  
            border-radius: 18px 18px 18px 0;  
            max-width: 75%;  
            margin: 5px 0;  
            box-shadow: 0 2px 8px rgba(245, 245, 220, 0.3);
        }
        
        .user-bubble:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4);
        }
        
        .bot-bubble:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(245, 245, 220, 0.4);
        }
        
        /* Chat container */
        .chat-container {  
            display: flex;  
            flex-direction: column;  
            gap: 5px;
        }  
        
        .botIcon {  
            background: linear-gradient(135deg, #ffab40 0%, #ff8f00 100%);
            color: #121212; 
            border-radius: 50%;  
            width: 50px; 
            height: 50px; 
            font-size: 28px; 
            text-align: center;  
            line-height: 50px; 
            flex-shrink: 0;
            box-shadow: 0 2px 6px rgba(255, 171, 64, 0.4);
        } 
        
        .userIcon {  
            background: linear-gradient(135deg, #3d7dd8 0%, #2a5db0 100%);
            color: white; 
            border-radius: 50%;  
            width: 50px; 
            height: 50px; 
            font-size: 28px; 
            text-align: center;  
            line-height: 50px; 
            flex-shrink: 0; 
            order: 2;
            box-shadow: 0 2px 6px rgba(61, 125, 216, 0.4);
        }
        
        /* Spinner animation */
        .spinner {
            display: inline-block;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>  
""", unsafe_allow_html=True) 

st.title("🤖 Chatbot - Abdelrahman Ahmed Sobhy") 

# Display all messages including any in-progress ones
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user": 
        st.markdown(f""" 
        <div class='chat-container'> 
            <div class='user-message-container'> 
                <div class='message'> 
                    <div class='user-bubble'>{msg['content']}</div> 
                    <div class='userIcon'>👤</div> 
                </div> 
            </div> 
        </div> 
        """, unsafe_allow_html=True) 
    else: 
        st.markdown(f""" 
        <div class='chat-container'> 
            <div class='message'> 
                <div class='botIcon'>🤖</div> 
                <div class='bot-bubble'>{msg['content']}</div> 
            </div> 
        </div> 
        """, unsafe_allow_html=True)

# Show thinking animation if processing
if st.session_state.processing:
    st.markdown(f""" 
    <div class='chat-container'> 
        <div class='message'> 
            <div class='botIcon'>🤖</div> 
            <div class='bot-bubble'>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="spinner">🤔</div>
                    <span>Thinking...</span>
                </div>
            </div> 
        </div> 
    </div> 
    """, unsafe_allow_html=True)

user_input = st.chat_input("Type your message here...") 
if user_input and not st.session_state.processing:
    # Add user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.processing = True
    st.rerun()  # Changed from experimental_rerun() to rerun()

# This runs after the rerun when processing is True
if st.session_state.processing and st.session_state.messages[-1]["role"] == "user":
    # Get the last user message
    user_message = st.session_state.messages[-1]["content"]
    
    # Get bot response
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask2",
            json={"question": user_message},
            timeout=10
        )
        
        if response.status_code == 200:
            bot_response = response.json()["answer"]
        else:
            bot_response = "Sorry, I encountered an error processing your request."
    except Exception as e:
        bot_response = f"Error connecting to the bot service: {str(e)}"
    
    # Add bot response and reset processing flag
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    st.session_state.processing = False
    st.rerun() 