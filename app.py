# __author__ = 'Andy'
# -*- coding: utf-8 -*-

import streamlit as st
# import adfun

st.set_page_config(
                    page_title="GT-Web_App_Demo",
                    # page_icon=icon,
                    layout="wide",
                    initial_sidebar_state="expanded",
                    page_icon=r"pics/logo/GT.png"
                   )

# st.title("HKIBIM_BIM_Automation_Arena_2025 - Master Challenge")

pages={
        "🌟Master Challenge": [
        st.Page(r"pages/Master Challenge Question.py", title="🌟- Question"),
        st.Page(r"pages/demo.py", title="🌟- Demo"),
                             ],      
}

pg=st.navigation(pages)


pg.run()

print("Andy")
