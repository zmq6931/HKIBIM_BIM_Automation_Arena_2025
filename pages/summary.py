import streamlit as st
import streamlit.components.v1 as components
from openai.types.chat import ChatCompletionMessage

import os
from openai import OpenAI
import pandas as pd






# from pandasai.llm import Grok




st.title("HKIBIM_BIM_Automation_Arena_2025 - Andy")
st.subheader("Summary")
video_expander=st.expander("Video") 
with video_expander:
    st.video(r"image/final_video/HKIBIM_AUTOMATION_MASTER_CHALLENGE_VIDEO_FINAL.mp4")
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
    st.write("### 20250328 3D V1")
    st.image(r"image/qrcode/qr_code_MasterChallenge_20250328.png",use_container_width=True)  
with col2:
    url="https://app.speckle.systems/projects/c3c82e786c/models/48646b195c"
    embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"   
    
    components.html(
        f"""
    <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
        """, 
    height=600  # Set the height explicitly for the component
    )

col1,col2=st.columns([1,3.5])
with col1:
    st.write("### 20250328 3D V2")
    st.image(r"image/qrcode/qr_code_MasterChallenge_20250328_v2.png",use_container_width=True)  
with col2:
    url="https://app.speckle.systems/projects/c3c82e786c/models/7f96d0a740"
    embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"   
    
    components.html(
        f"""
    <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
        """, 
    height=600  # Set the height explicitly for the component
    )



st.divider()

st.write("### GitHub")
st.write("- HKIBIM_Automation_2025_Demo2_Grasshopper_Plugins -> https://github.com/zmq6931/HKIBIM_Automation_2025_Demo2_Grasshopper_Plugins.git")
st.write("- HKIBIM_BIM_Automation_Arena_2025 -> Master Challenge 2025 -> https://github.com/zmq6931/HKIBIM_BIM_Automation_Arena_2025.git")
st.image(r"image/others/github_pic1.png",width=1000)
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
### Standards? Just the foundation—critical, yes, but basic. Automation is the unstoppable core of BIM (Building Information Modeling), powering efficiency and precision, obliterating tedious tasks, and supercharging workflows. Breakthroughs and innovation? They're the blazing soul of BIM, shattering limits, igniting bold creativity, and unleashing game-changing possibilities. But make no mistake—the BIMer is the ultimate force here. They don't just use these tools, they command them, fusing structure, efficiency, and genius into a revolution. BIM isn't just a process—it's a powerhouse, and the fearless BIMer drives its true, world-shaping potential.
    
# What is the most important -> BIMer
    """
)

st.divider()
st.write("### AI Chat")






dfTransoms=pd.read_csv("pages/transoms.csv")

# df_dict = dfTransoms.to_dict(orient='records')

client = OpenAI(
    api_key=st.secrets["grok_ad_test_001_apikey"], 
    base_url=st.secrets["grok_api_url"],
)
model="grok-2-latest"


# client = OpenAI(
#     api_key=st.secrets["deepseek_apikey"], 
#     base_url=st.secrets["deepseek_api_url"],
# )
# model="deepseek-chat"


# if "messages_2" not in st.session_state:
#     st.session_state.messages_2 = []


#region Chat 1
ai_expander1=st.expander("AI Chat1 - Test deepseek api and grok api ")

with ai_expander1:
    if "messages_1" not in st.session_state:
        st.session_state.messages_1 = []
    for message in st.session_state.messages_1:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Chat 1: What is up?", key="chat_input_1"):
        st.session_state.messages_1.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        completion = client.chat.completions.create(
            model=model,
            # model="grok-2-latest",
            messages=[
                {"role": "system", "content": f"You are a PhD-level mathematician and BIMer. your data is {dfTransoms}"},
                *({"role": m["role"], "content": m["content"]} for m in st.session_state.messages_1)
            ],
            stream=True
        )
        
        response = st.write_stream(completion)
        st.session_state.messages_1.append({"role": "assistant", "content": response})


#endregion

#region Chat 2




ai_expander2=st.expander("AI Chat2 - PandasAI - use pandasai free apikey")
with ai_expander2:

    import pandasai as pai

    pai.api_key.set(st.secrets["pandasai_apikey"])
    file = pai.read_csv(r"pages/transoms.csv")
    # file = pai.load("pai-personal-3f69d/dataset-name")
    st.write(file)
    input_text=st.text_area("input")
    botton=st.button("submit")
    # st.write(input_text)
    if botton:
        result=pai.chat(input_text,file)
        if isinstance(result,pd.DataFrame):
            st.dataframe(result)
        elif isinstance(result,str):
            if result.lower().endswith((".png",".jpg",".jpeg")):
                st.image(result)
            else:
                st.write(result)
        elif isinstance(result,(int,float)):
            st.write(result)
        else:
            st.write(result)
    

    



    
    # 使用 GrokLLM 创建 SmartDataframe

#endregion
    

#region Chat 3 
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_community.chat_models import ChatOpenAI  # 我们暂时用这个模拟，需替换为 xAI 的实现
from langchain.agents.agent_types import AgentType
import sys
from io import StringIO

old_stdout = sys.stdout
sys.stdout = captured_output = StringIO()

ai_expander3=st.expander("AI Chat3 - langchain - create_csv_agent - xai")
with ai_expander3:
    input_text=st.text_area("input",height=100)
    botton=st.button("submit",key="submit_botton")
    if botton:
        llm = ChatOpenAI(
        api_key=st.secrets["grok_ad_test_001_apikey"],
        model="grok-2-latest",  
        temperature=1,
        base_url=st.secrets["grok_api_url"]  
        )

        agent = create_csv_agent(
            llm,
            r"pages/transoms.csv",  
            verbose=True,   
            agent_type="zero-shot-react-description",
            # agent_type="zero-shot-react-description",
            # agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            include_df_in_prompt=True,
            allow_dangerous_code=True,  
            handle_parsing_errors=True,
            max_iterations=1,
        )
        question = input_text
        response = agent.invoke({"input": question})
        
        
        
        sys.stdout = old_stdout
        verbose_output = captured_output.getvalue()
        print(verbose_output)


        output_lines = verbose_output.split("\n")
        thought = ""
        observation = ""
        for line in output_lines:
            if "Thought:" in line:
                thought = line.split("Thought:")[1].strip()
            # elif "Observation" in line:
            #     observation = line.split("Observation")[1].strip()

        st.write(thought)
        # st.write(output_lines)
        if "Observation[0m" in verbose_output and "[36;1m[1;3mNameError:" in verbose_output:
            observation=verbose_output.split("Observation[0m")[1].split("[36;1m[1;3mNameError:")[0]
            st.write(observation)
        else:            
            # st.write(verbose_output)
            st.write(output_lines)
            st.write(verbose_output)
        
        
        # try:
        #     observation=verbose_output.split("Observation[0m")[1].split("[36;1m[1;3mNameError:")[0]
        # except:
        #     pass
            
        # st.write(observation)
        # st.write("aaa")
        
#endregion  
print(dfTransoms["length"].sum())






