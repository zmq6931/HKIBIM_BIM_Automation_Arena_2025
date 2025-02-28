import streamlit as st
import streamlit.components.v1 as components
from openai.types.chat import ChatCompletionMessage

st.title("HKIBIM_BIM_Automation_Arena_2025 - Andy")
st.subheader("Summary")
st.divider()

col1,col2,col3=st.columns([1,1,1])
with col1:
    st.write("""
    ## 1. Multi-software integration   
    - Digital Project
    - AutoCAD
    - Rhinoceros
    - Grasshopper
    - Tekla
    - Navisworks
    - Matlab
    - Cursor
    - Visual Studio
    - Speckle
""")
with col2:
    st.write("""
    ## 2. Programming Language
    - Python
        - Streamlit
        - pywin32
        - pyxll
        - plotly
        - rhinoscriptsyntax
        - matlabengine==24.2.2
        - pandas
        - C#
        - Tekla.Structures
        - Tekla.Structures.Model
        - Grasshopper
    """)
with col3:
    st.write("""
    ## 3. AI Assistant
    - Cursor
        - deepseek-v3
        - deepseek-r1
        - gpt-4o-mini        
    - deepseek
    - Grok
    - ChatGPT
    - Codeium
    - Perplexity    
    """)

st.divider()

col1,col2=st.columns([1,3.5])
with col1:
    st.write("### demo3_solution3")
    st.image(r"image/qrcode/qr_code_demo3_solution3.png",use_container_width=True)  
with col2:
    url="https://app.speckle.systems/projects/c3c82e786c/models/d5dc8ed71e"
    embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"   
    
    components.html(
        f"""
    <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
        """, 
    height=600  # Set the height explicitly for the component
    )

st.divider()
# st.markdown("""
# ### - BIM is not a single software, it's a collaborative process that requires multiple software tools from project start to finish, leveraging the strengths of each software, forming a complete workflow or solution from the design phase through to completion and even operation and maintenance.
# ### - BIM is a process that continuously evolves, iterates, and optimizes with the development of software, hardware, and the experience of project team members.
# ### - BIM is also big data. BIMer need to handle massive amounts of model data, information data, etc., which also means automation is inevitable.
# ### - BIM needs to meet certain standards because high standardization leads to high automation, but more importantly, breakthroughs and innovation are the soul of BIM.

# # What is the most important -> BIMer
# """)
st.write(
    """
### Standards? Just the foundation—critical, yes, but basic. Automation is the unstoppable core of BIM (Building Information Modeling), powering efficiency and precision, obliterating tedious tasks, and supercharging workflows. Breakthroughs and innovation? They’re the blazing soul of BIM, shattering limits, igniting bold creativity, and unleashing game-changing possibilities. But make no mistake—the BIMer is the ultimate force here. They don’t just use these tools, they command them, fusing structure, efficiency, and genius into a revolution. BIM isn’t just a process—it’s a powerhouse, and the fearless BIMer drives its true, world-shaping potential.
    
# What is the most important -> BIMer
    """
)

st.divider()
st.write("### AI Chat")




import os
from openai import OpenAI
import pandas as pd

dfTransoms=pd.read_csv("pages/transoms.csv")
client = OpenAI(
    api_key=st.secrets["grok_ad_test_001_apikey"], 
    base_url=st.secrets["grok_api_url"],
)

ai_container=st.container()

with ai_container:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


        # Generate a response using the OpenAI API.
        completion = client.chat.completions.create(
            model="grok-2-latest",
            messages=[
                {"role": "system", "content": f"You are a PhD-level mathematician. your data is {dfTransoms}"},
                *({"role": m["role"], "content": m["content"]} for m in st.session_state.messages)
            ],
            stream=True
        )


        
        response = st.write_stream(completion)
        st.session_state.messages.append({"role": "assistant", "content": response})






