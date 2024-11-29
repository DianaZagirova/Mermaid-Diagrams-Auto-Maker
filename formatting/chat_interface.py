import streamlit as st

def handle_userInput(chat_history):   
    for i, msg in enumerate(chat_history[::-1]):            
        if i % 2 == 0:
            st.markdown(
            f"""
            <div style="
                border: 0px solid #1a73e8;
                fornt-weight: 2;
                border-radius: 7px;
                padding: 10px;
                display: flex;
                align-items: flex-start; /* Align items to the top */
                justify-content: flex-end; /* Align messages to the right */
                color: #1a73e8; /* Change text color to blue for user question */
            ">                
                <div style="margin-left: 10px; margin-bottom: 5px; margin-top: 10px;">  
                {msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        else:
            with st.expander("Bot answer"):
                st.markdown(
            f"""
            <div style="
                border: 1px solid #1a73e8;
                border-radius: 7px;
                padding: 10px;
                display: flex;
                align-items: flex-start; /* Align items to the top */
                color: black; /* Change text color to black for answer */
            ">
                <img src="https://img.icons8.com/sf-regular/48/message-bot.png" alt="message-bot" style="
                    width: 29px;  /* Adjust the size as needed */
                    height: 29px;  /* Adjust the size as needed */
                    border-radius: 50%;  /* Makes the image round */
                    margin-right: 3px;
                    float: left; /* Aligns the image to the left */
                    filter: hue-rotate(10deg) saturate(100%);
                ">
                <div style="margin-left: 10px; margin-bottom: 10px;">  
                {msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )