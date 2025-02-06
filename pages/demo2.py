import streamlit as st
import pythoncom
try:
    import adfun as adfun
except:
    from importlib.machinery import SourceFileLoader
    adfun = SourceFileLoader("module.name",r"adfun.py").load_module()




st.title("HKIBIM_BIM_Automation_Arena_2025")
st.subheader("Master Challenge Demo2")



pythoncom.CoInitialize()
dp=adfun.mydpfun.getDpApplication()
doc=dp.ActiveDocument
osel=doc.Selection
part=doc.Part
hsf=part.HybridShapeFactory
parameters=part.Parameters
panel_W=parameters["panel_W"]
panel_L=parameters["panel_L"]
pt_Distance=parameters["pt_Distance"]
resultGeo=part.HybridBodies.item("ResultGeo")
curveGeo=part.HybridBodies.item("curves")









    