import streamlit as st
import pythoncom
try:
    import adfun as adfun
except:
    from importlib.machinery import SourceFileLoader
    adfun = SourceFileLoader("module.name",r"adfun.py").load_module()




st.title("HKIBIM_BIM_Automation_Arena_2025 - Andy")
st.subheader("Master Challenge Demo2")

st.divider()
st.write("### Why Demo2 and step 1 sell generation")
why_demo2_expander=st.expander("Why Demo2 and step 1 sell generation")
with why_demo2_expander:
    st.write("### Why Demo2")

    col1,col2,col3=st.columns([0.8,1.1,1])
    with col1:
        st.write("""
             Why is there a demo2? It's because this shape looks like a little bird, and bimer is like this bird, trying to break out of its shell. That shell represents standards or outdated ideas.
    """)
    with col2:
        st.image(r"image/deom2/demo2.png")
    with col3:
        st.image(r"image/deom2/shape2.png")

st.divider()
st.write("### Step 2 panel automation")
step2_expander=st.expander("Step 2 panel automation")
with step2_expander:
    st.write("### Step 2 panel automation")
    st.video(r"image\deom2\rhino_panel_generation.mp4")














    