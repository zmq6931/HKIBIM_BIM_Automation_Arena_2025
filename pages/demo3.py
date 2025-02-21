import streamlit as st
import streamlit.components.v1 as components

st.title("HKIBIM_BIM_Automation_Arena_2025 - Andy")
st.subheader("Master Challenge Demo3")
st.divider()

st.write("### demo1 + demo2 -> demo3")
col1,col2=st.columns([1,2.6])
with col1:
    st.markdown("<h3 style='color:red;'>demo1</h3>", unsafe_allow_html=True)
    st.image(r"image/demo3/pic1.png")
    st.markdown("<h3 style='color:red;'>demo2</h3>", unsafe_allow_html=True)
    st.image(r"image/demo3/pic2.png")
with col2:
    st.markdown("<h3 style='color:red;'>demo3</h3>", unsafe_allow_html=True)
    st.image(r"image/demo3/pic3.png",use_container_width=True)
    
st.divider()

st.write("### Result 3D ")
result_expander_demo3_solution1=st.expander("demo3_solution1")
with result_expander_demo3_solution1:
    col1,col2=st.columns([1,3.5])
    with col1:
        st.write("### demo3_solution1")
        st.image(r"image/qrcode/qr_code_demo3_solution1.png",use_container_width=True)
    with col2:
        url="https://app.speckle.systems/projects/c3c82e786c/models/ca8df4dd08"
        embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"
        
        components.html(
            f"""
        <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
            """, 
        height=600  # Set the height explicitly for the component
        )

result_expander_demo3_solution2=st.expander("demo3_solution2")
with result_expander_demo3_solution2:
    col1,col2=st.columns([1,3.5])
    with col1:
        st.write("### demo3_solution2")
        st.image(r"image/qrcode/qr_code_demo3_solution2.png",use_container_width=True)
    with col2:
        url="https://app.speckle.systems/projects/c3c82e786c/models/6bcaed5785"
        embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"   
        
        components.html(
            f"""
        <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
            """, 
        height=600  # Set the height explicitly for the component
        )

result_expander_demo3_solution3=st.expander("demo3_solution3")
with result_expander_demo3_solution3:
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





