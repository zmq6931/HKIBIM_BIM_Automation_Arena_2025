import streamlit as st

st.title("HKIBIM_BIM_Automation_Arena_2025")

st.subheader("Master Challenge Demo")

#region step1
st.write("## 1. Extract wireframe from rhino model")

st.expander("Extract wireframe from rhino model")
with st.expander("Extract wireframe from rhino model"):
    col1,col2=st.columns(2)
    with col1:
        st.image(r"image/step1/pic1.png")
    with col2:
        st.image(r"image/step1/pic2.png")

#endregion

#region step2
st.write("## 2. Smooth curves")
st.expander("Smooth curves")
with st.expander("Smooth curves"):
    col1,col2=st.columns(2)
    with col1:
        st.image(r"image/step2/pic1.png")
    with col2:
        st.image(r"image/step2/pic2.png")
#endregion





