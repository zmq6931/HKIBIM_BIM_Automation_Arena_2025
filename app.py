# __author__ = 'Andy'
# -*- coding: utf-8 -*-

import streamlit as st
# import adfun

st.set_page_config(
                    page_title="MasterChallenge_Andy_Demo",
                    # page_icon=icon,
                    layout="wide",
                    initial_sidebar_state="expanded",
                    page_icon=r"pics/logo/GT.png"
                   )

# st.title("HKIBIM_BIM_Automation_Arena_2025 - Master Challenge")

pages={
        "🌟Master Challenge": [
        st.Page(r"pages/Master Challenge Question.py", title="🌟- Question"),
        st.Page(r"pages/demo1.py", title="🌟- Demo1"),
        st.Page(r"pages/demo2.py", title="🌟- Demo2"),
        st.Page(r"pages/demo3.py", title="🌟- Demo3"),
                             ],      
}

pg=st.navigation(pages)


pg.run()

print("ad")



