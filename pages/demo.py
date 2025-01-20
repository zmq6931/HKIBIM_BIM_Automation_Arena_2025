import streamlit as st
import pythoncom
try:
    import adfun as adfun
except:
    from importlib.machinery import SourceFileLoader
    adfun = SourceFileLoader("module.name",r"adfun.py").load_module()
   



st.title("HKIBIM_BIM_Automation_Arena_2025")
st.subheader("Master Challenge Demo")


#region 1. Extract wireframe from rhino model
st.write("### 1. Extract wireframe from rhino model")

st.expander("Extract wireframe from rhino model")
with st.expander("Extract wireframe from rhino model"):
    col1,col2=st.columns(2)
    with col1:
        st.image(r"image/step1/pic1.png")
    with col2:
        st.image(r"image/step1/pic2.png")

#endregion

#region 2. Smooth curves
st.write("### 2. Smooth curves")
st.expander("Smooth curves")
with st.expander("Smooth curves"):
    col1,col2=st.columns(2)
    with col1:
        st.image(r"image/step2/pic1.png")
    with col2:
        st.image(r"image/step2/pic2.png")
#endregion

st.divider()

#region 3. demo1 test   
st.write("### 3. demo1 test")
#endregion

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

    
# print(width.Value, length.Value, height.Value)
st.write("current doc name is -> ", doc.name)
if doc.name=="s02_demo1.CATPart":   
    
    #region 4. Main parameter
    st.markdown("<h3 style='color: red;'>4. Main parameter</h3>", unsafe_allow_html=True)
    # st.write("default parameters: 1000, 2500, 700")
    col1,col2,col3=st.columns(3)
    with col1:
        input_panel_W = st.number_input("panel_W",min_value=300,value=1000,step=100)
    with col2:
        input_panel_L = st.number_input("panel_L", min_value=2000,value=2500,step=100)
    with col3:
        input_pt_Distance = st.number_input("pt_Distance",min_value=200,value=700,step=50)
        
    
    btn_change_parameter=st.button("Change Parameter",use_container_width=True)
    if btn_change_parameter:
        st.write("panel_W: ",input_panel_W,"panel_L: ",input_panel_L,"pt_Distance: ",input_pt_Distance)
        panel_W.Value=input_panel_W
        panel_L.Value=input_panel_L
        pt_Distance.Value=input_pt_Distance
    
    #region 5. Generate Points
    st.write("### 5. Generate Points")
    btn_generate_points=st.button("Generate Points",use_container_width=True)
    pointsGeo=None
    if btn_generate_points:
        try:
            pointsGeo=resultGeo.HybridBodies.item("pointsGeo")
        except:
            pointsGeo=resultGeo.HybridBodies.Add()
            pointsGeo.Name="pointsGeo"

        for curve in curveGeo.HybridShapes:
            tempgeo=pointsGeo.HybridBodies.Add()
            tempgeo.Name=curve.Name+"_points"
            
            # adfun.mydpfun.call_catscript_or_catvbs(
            #     dp,
            #     catscript_folder=r"C:\Andy\pycode\Andy_Python\CATScript", 
            #     CATScript_fileName="adfun_catia.catvbs",
            #     functionName="PointsOnCurveInsertedByPointDistance",
            #     parameters=[osel,hsf,tempgeo,curve,pt_Distance.Value,True,-1],
            #     CatScriptLibraryType =1)
            adfun.mydpfun.call_catscript_or_catvbs(
                dp,
                catscript_folder=r"C:\Andy\pycode\Andy_Python\CATScript", 
                CATScript_fileName="adfun_catia.catvbs",
                functionName="PointsOnCurveInsertedByPointDistance2",
                parameters=[part,hsf,tempgeo,curve,pt_Distance.Value],
                CatScriptLibraryType =1)

    #endregion

    #region 6. Generate Panel
    st.write("### 6. Generate Panel")
            
    pointsGeo=resultGeo.HybridBodies.item("pointsGeo")
    
    btn_generate_panel=st.button("Generate Panels",use_container_width=True)
    if btn_generate_panel:
        try:
            panelsGeo=resultGeo.HybridBodies.item("panelsGeo")
        except:
            panelsGeo=resultGeo.HybridBodies.Add()
            panelsGeo.Name="panelsGeo"

        for i in range(1,len(pointsGeo.HybridBodies)):
            tempPointsGeo1=pointsGeo.HybridBodies.item(i)
            tempPointsGeo2=pointsGeo.HybridBodies.item(i+1)
            tempgeo=panelsGeo.HybridBodies.Add()
            curve2=curveGeo.HybridShapes.item(i+1)

            tempgeo.Name="PanelGeo_"+str(i)
            for j in range(1,len(tempPointsGeo1.HybridShapes)):
                pt1=tempPointsGeo1.HybridShapes.item(j)
                pt2=tempPointsGeo1.HybridShapes.item(j+1)
                ptdir=hsf.AddNewPointOnCurveWithReferenceFromPercent(curve2,pt1,0,False)#
                distance=adfun.mydpfun.measure.measureTwoObjectMinDistance(doc,pt1,pt2)
                extend_length=(panel_W.Value-distance)/2
                line=hsf.AddNewLinePtPtExtended(pt1,pt2,extend_length,extend_length)
                
                tempgeo.AppendHybridShape(line)

            part.Update()

                
            break  


    #endregion 
    
    
    



    print("finished")