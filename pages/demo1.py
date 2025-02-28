import streamlit as st
import pythoncom
import pandas as pd
import plotly.express as px
import math
import array
import os,sys
import streamlit.components.v1 as components

try:
    import adfun as adfun
except:
    from importlib.machinery import SourceFileLoader
    adfun = SourceFileLoader("module.name",r"adfun.py").load_module()
   


def distance_3d(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

def dimensionPtPt(modelSpace, pt1,pt2, TextPosition,TextHeight=100):
    dimension1= modelSpace.AddDimAligned(pt1,pt2,TextPosition)
    dimension1.TextHeight=TextHeight

st.title("HKIBIM_BIM_Automation_Arena_2025 - Andy")
st.subheader("Master Challenge Demo1")


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
width=parameters["Width"]
length=parameters["Length"]
height=parameters["Height"]
resultGeo=part.HybridBodies.item("ResultGeo")
curveGeo=part.HybridBodies.item("curves")

dp.DisplayFileAlerts=False
    
# print(width.Value, length.Value, height.Value)
st.write("current doc name is -> ", doc.name)

# if True:  #if doc.name=="s02_demo1.CATPart":    

    
#region 4. Main parameter
st.markdown("<h3 style='color: red;'>4. Main parameter</h3>", unsafe_allow_html=True)
# st.write("default parameters: 1000, 2500, 700")
col1,col2,col3=st.columns(3)
with col1:
    input_panel_W = st.number_input("panel_W",min_value=300,value=1500,step=100)
with col2:
    input_panel_L = st.number_input("panel_L", min_value=2000,value=2500,step=100)
with col3:
    input_pt_Distance = st.number_input("pt_Distance",min_value=200,value=1200,step=50)
    
col1,col2,col3=st.columns(3)
with col1:
    input_Width = st.number_input("Width",min_value=40000,value=47000,step=100)
with col2:
    input_Length = st.number_input("Length", min_value=60000,value=69800,step=100)
with col3:
    input_Height = st.number_input("Height",min_value=13000,value=18000,step=50)
    
btn_change_parameter=st.button("Change Parameter",use_container_width=True)
if btn_change_parameter:
    st.write("panel_W: ",input_panel_W,"panel_L: ",input_panel_L,"pt_Distance: ",input_pt_Distance)
    st.write("Width: ",input_Width,"Length: ",input_Length,"Height: ",input_Height)
    panel_W.Value=input_panel_W
    panel_L.Value=input_panel_L
    pt_Distance.Value=input_pt_Distance
    width.Value=input_Width
    length.Value=input_Length
    height.Value=input_Height
    
    part.Update()

btn_saveas_iges=st.button("Save as IGES",use_container_width=True)
if btn_saveas_iges:
    st.write("Saving as IGES...")
    export_path=r"C:\Andy\Andy_Collection\AndyZMQ_Personal\2025_Automation\Master_Challenge\temp_surfaces.igs"
    name=export_path.split('.')[0]
    format=export_path.split('.')[1]
    doc.ExportData(name,format)

    
    

        

#endregion

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
        
        adfun.mydpfun.call_catscript_or_catvbs(
            dp,
            catscript_folder=r"C:\Andy\pycode\Andy_Python\CATScript", 
            CATScript_fileName="adfun_catia.catvbs",
            functionName="PointsOnCurveInsertedByPointDistance2",
            parameters=[part,hsf,tempgeo,curve,pt_Distance.Value],
            CatScriptLibraryType =1)

Generate_Points_expander=st.expander("Generate_Points_expander")
with Generate_Points_expander:
    st.video(r"image/demo1_step5/generate points_2.mp4",format="video/mp4",autoplay=True,loop=True)
#endregion

#region 6. Generate Panel
st.write("### 6. Generate Panel")
        

btn_generate_panel=st.button("Generate Panels",use_container_width=True)
i=0
offset_distance=500

if btn_generate_panel:
    pointsGeo=resultGeo.HybridBodies.item("pointsGeo")
    scopebody=part.Bodies.item("scope_solid")
    scope=scopebody.Shapes.item("scope")
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

            
        dif_row_distance=100
        for j in range(1,len(tempPointsGeo1.HybridShapes)):
            pt1=tempPointsGeo1.HybridShapes.item(j)
            pt2=tempPointsGeo1.HybridShapes.item(j+1)
            curve2Pt=hsf.AddNewPointOnCurveWithReferenceFromPercent(curve2,pt1,0,False)
            # dir=adfun.mydpfun.direction.getDirectionByPlaneOrLine(hsf,hsf.AddNewLinePtPt(pt1,curve2Pt))
            distance=adfun.mydpfun.measure.measureTwoObjectMinDistance(doc,pt1,pt2)
            extend_length=(panel_W.Value-distance)/2
            line=hsf.AddNewLinePtPtExtended(pt1,pt2,extend_length,extend_length)
            dirline=hsf.AddNewLineAngle(line,None,curve2Pt,True,0,panel_L.Value,90,True)
            dir=adfun.mydpfun.direction.getDirectionByPlaneOrLine(hsf,dirline)
            extrude=hsf.AddNewExtrude(line,panel_L.Value,0,dir)
            if i%2==0:
                if j%2==0:
                    offset=hsf.AddNewOffset(extrude,offset_distance+dif_row_distance,False,0)
                else:
                    offset=hsf.AddNewOffset(extrude,offset_distance+200+dif_row_distance,False,0)
                offset.Name="offset_R"+str(i).zfill(3)+"_N"+str(j).zfill(3)
                tempgeo.AppendHybridShape(offset)
            else:
                if j%2==0:
                    offset=hsf.AddNewOffset(extrude,offset_distance,False,0)
                else:
                    offset=hsf.AddNewOffset(extrude,offset_distance+200,False,0)
                offset.Name="offset_R"+str(i).zfill(3)+"_N"+str(j).zfill(3)
                tempgeo.AppendHybridShape(offset)
            

        part.Update()
        
        for shape in tempgeo.HybridShapes:
            distance=adfun.mydpfun.measure.measureTwoObjectMinDistance(doc,scope,shape)
            if distance<1:
                osel.clear()
                osel.add(shape)
                osel.delete()
            
        # if i>2:                
        #     break  

Generate_Panels_expander=st.expander("Generate_Panels_expander")
with Generate_Panels_expander:
    st.video(r"image/demo1_step6/generatePanel_2.mp4",format="video/mp4",autoplay=True,loop=True)
#endregion

#region 7. Generate Transoms
st.write("### 7. Generate Steel frames")
transom_pt1_distance=1000

btn_generate_transoms=st.button("Generate Steel frames",use_container_width=True)
if btn_generate_transoms:
    transomsGeo=None
    try:
        transomsGeo=resultGeo.HybridBodies.item("transomsGeo")
    except:
        transomsGeo=resultGeo.HybridBodies.Add()
        transomsGeo.Name="transomsGeo"
    transom_curves_Geo=part.HybridBodies.item("transom_curves")
    for geo in transom_curves_Geo.HybridBodies:
        tempgeo=transomsGeo.HybridBodies.Add()
        tempgeo.Name=geo.Name
        # if geo.Name=="transom_curvesL1":
        for i in range(1,len(geo.HybridShapes)):
            subgeo=tempgeo.HybridBodies.Add()
            subgeo.Name=geo.Name+"_"+str(i).zfill(3)
            curve1=geo.HybridShapes.item(i)
            curve2=geo.HybridShapes.item(i+1)
            curveLength=adfun.mydpfun.measure.measureGetLength(curve1)
            # calculate the number of points on the curve-------------------------------------------
            ptcount=int(curveLength/panel_W.Value)+2+1
            for j in range(1,ptcount+1):
                pt1=hsf.AddNewPointOnCurveFromPercent(curve1,(j-1)/(ptcount-1),True)
                pt1.Name=subgeo.Name+"_line_"+str(j).zfill(3)+"_pt1"
                # pt2=hsf.AddNewPointOnCurveWithReferenceFromPercent(curve2,pt1,0,False)
                pt2=hsf.AddNewPointOnCurveFromPercent(curve2,(j-1)/(ptcount-1),True)
                pt2.Name=subgeo.Name+"_line_"+str(j).zfill(3)+"_pt2"
                line=hsf.AddNewLinePtPt(pt1,pt2)
                line.Name=subgeo.Name+"_line_"+str(j).zfill(3)
                sweepCircle=adfun.mydpfun.create.create_SweepCircle_Surface(part,hsf,subgeo,line,100)
                sweepCircle.Name=subgeo.Name+"_"+str(j).zfill(3)
                # referenceLine=part.CreateReferenceFromObject(line)
                # sweepCircle=hsf.AddNewSweepCircle(referenceLine)
                # sweepCircle.Mode=6
                
                # sweepCircle.SetRadius(1,100)
                # subgeo.AppendHybridShape(sweepCircle)
        part.Update() 
        # break   
Generate_Transoms_expander=st.expander("Generate_SteelFrames_expander")
with Generate_Transoms_expander:
    st.video(r"image/demo1_step7/transomGenerate_2.mp4",format="video/mp4",autoplay=True,loop=True)
#endregion

#region 8. Extract Information



st.write("### 8. Extract Information")
btn_extract_information=st.button("Extract Information",use_container_width=True)
if btn_extract_information:
    transomsGeo=resultGeo.HybridBodies.item("transomsGeo")
    osel.clear()
    osel.add(transomsGeo)
    osel.Search("Name=*pt*,sel")
    pts = adfun.mydpfun.selection.selectionToArray(osel)
    osel.clear()
    dfTransoms=pd.DataFrame()
    name=[]
    length=[]
    # startPoint=[]
    # endPoint=[]
    pt1x=[]
    pt1y=[]
    pt1z=[]
    pt2x=[]
    pt2y=[]
    pt2z=[]
    
    for i in range(0,int(len(pts)/2)):
        name.append(pts[i*2].Name.replace("_pt1",""))
        pt1coord= adfun.mydpfun.measure.getPointCoords(dp,pts[i*2])
        pt1x.append(pt1coord[0])
        pt1y.append(pt1coord[1])
        pt1z.append(pt1coord[2])
        pt2coord= adfun.mydpfun.measure.getPointCoords(dp,pts[i*2+1])
        pt2x.append(pt2coord[0])
        pt2y.append(pt2coord[1])
        pt2z.append(pt2coord[2])
        distance=distance_3d((pt1coord[0],pt1coord[1],pt1coord[2]),(pt2coord[0],pt2coord[1],pt2coord[2]))
        length.append(distance)
        
    dfTransoms["name"]=name
    dfTransoms["length"]=length
    dfTransoms["pt1x"]=pt1x
    dfTransoms["pt1y"]=pt1y
    dfTransoms["pt1z"]=pt1z
    dfTransoms["pt2x"]=pt2x
    dfTransoms["pt2y"]=pt2y
    dfTransoms["pt2z"]=pt2z
    st.dataframe(dfTransoms)
    dfCount=pd.DataFrame()
    name=["panelCount","transomCount"]
    osel.clear()
    osel.add(resultGeo.HybridBodies.item("panelsGeo"))
    osel.Search("Name=offset_*,sel")
    panelCount=osel.count
    osel.clear()
    transomsCount=len(pts)/2
    count=[panelCount,transomsCount]
    dfCount["name"]=name
    dfCount["count"]=count
    fig = px.bar(dfCount, x='name', y='count',color="name", title='Count of Panels and Transoms')
    st.plotly_chart(fig,use_container_width=True)
    
    fig2=px.line(dfTransoms,x="name",y="length",title="Transoms Length")
    st.plotly_chart(fig2,use_container_width=True)
    dfTransoms.to_csv("pages/transoms.csv",index=False)
Extract_Information_expander=st.expander("Extract_Information_expander")
with Extract_Information_expander:
    st.video(r"image/demo1_extract_information/extract_information.mp4",format="video/mp4",autoplay=True,loop=True)
    st.image(r"image/demo1_extract_information/pic1.png")
#endregion


#region 9. Drawing Generation
st.write("### 9. Drawing Generation")

btn_drawing_generation=st.button("Drawing Generation",use_container_width=True)
if btn_drawing_generation:
    app=adfun.mycadfun.getAutocadApp()
    doc=adfun.mycadfun.getActiveDocument(app)
    modelSpace=adfun.mycadfun.getModelSpace(doc)
    # adfun.mycadfun.createPointByCoords(modelSpace,1,1,1)
    pt1=array.array('d',[0,0,0])
    pt2=array.array('d',[panel_W.Value,0,0])
    pt3=array.array('d',[0,panel_L.Value,0])
    pt4=array.array('d',[panel_W.Value,panel_L.Value,0])
    line1=modelSpace.AddLine(pt1,pt2)
    line2=modelSpace.AddLine(pt1,pt3)
    line3=modelSpace.AddLine(pt2,pt4)
    line4=modelSpace.AddLine(pt3,pt4)       

    position1=array.array('d',[(pt1[0]+pt2[0])/2,(pt1[1]+pt2[1])/2-120,(pt1[2]+pt2[2])/2])
    position2=array.array('d',[(pt2[0]+pt4[0])/2+120,(pt2[1]+pt4[1])/2,(pt2[2]+pt4[2])/2])
    position3=array.array('d',[(pt1[0]+pt3[0])/2-120,(pt1[1]+pt3[1])/2,(pt1[2]+pt3[2])/2])
    position4=array.array('d',[(pt3[0]+pt4[0])/2,(pt3[1]+pt4[1])/2+120,(pt3[2]+pt4[2])/2])
    position5=array.array('d',[(pt1[0]+pt4[0])/2,(pt1[1]+pt4[1])/2,(pt1[2]+pt4[2])/2])
    position6=array.array('d',[(pt2[0]+pt3[0])/2,(pt2[1]+pt3[1])/2,(pt2[2]+pt3[2])/2])
    dimension1= dimensionPtPt(modelSpace,pt1,pt2,position1)    
    dimension2= dimensionPtPt(modelSpace,pt2,pt4,position2)
    dimension3= dimensionPtPt(modelSpace,pt1,pt3,position3)
    dimension4= dimensionPtPt(modelSpace,pt3,pt4,position4)
    dimension5= dimensionPtPt(modelSpace,pt1,pt4,position5)
    dimension6= dimensionPtPt(modelSpace,pt2,pt3,position6)

    
    
    doc.Regen(0)
    
    
    
    st.write(doc.Name)
drawing_expander=st.expander("Drawing_Expander")    
with drawing_expander:
    st.video(r"image/demo1_drawing_generation/drawing_generation.mp4",format="video/mp4",autoplay=True,loop=True)
        
    
#endregion

#region 10. Lighting
st.write("### 10. Lighting")
btn_lighting=st.button("Lighting",use_container_width=True)
if btn_lighting:
    import os
    import matlab.engine
    eng=matlab.engine.start_matlab()
    eng.run(r"C:\Andy\github\HKIBIM_BIM_Automation_Arena_2025\mat\matlab_demo1.m",nargout=0)
lighting_expander=st.expander("Lighting_Expander")    
with lighting_expander:
    col1,col2=st.columns(2)
    with col1:
        st.image(r"image/demo1_lighting/pic2.png")
    with col2:
        st.image(r"image/demo1_lighting/pic3.png")
    st.divider()
    st.video(r"image/demo1_lighting/lighting.mp4",format="video/mp4",autoplay=True,loop=True)
    st.divider()    
    code="""
data=readtable('demo1.csv');

x1=data.pt1x;   
y1=data.pt1y;
z1=data.pt1z;
x2=data.pt2x;
y2=data.pt2y;
z2=data.pt2z;

colormap(jet);
colorbar;
h1 = scatter3(x1, y1, z1,30,z1, 'filled');
axis equal;
hold on;
h2 = scatter3(x2, y2, z2,30,z2, 'filled');
xlabel('X');
ylabel('Y');
zlabel('Z');
title('3D Point Animation from Blue to White');
grid on;
% count=numel(x1);
% animationTime = 20; 
% j = 1; 

frames=5000;
for t=1:frames
    color_shift = sin(2 * pi * t / frames);
    c = (y1 - min(y1)) / (max(y1) - min(y1));
    c = c + color_shift;
    c = mod(c, 1);
    h1.CData = c;
    h2.CData = c;
    pause(0.0005);
end
    """
    
    # st.markdown(f'<div class="code-container"><pre>{code}</pre></div>', unsafe_allow_html=True)

    st.code(code,language="matlab",wrap_lines=True)
#endregion

#region 11. Greenery
st.write("### 11. Greenery")
Greenery_expander=st.expander("Greenery_Expander")
with Greenery_expander:
    col1,col2=st.columns([1.5,2.2],border=True)
    with col1:
        st.write("Solution 1")
        st.image(r"image/demo1_greenery/pic1.png")
        st.image(r"image/demo1_greenery/pic2.png")
    with col2:
        st.write("Solution 2")
        st.image(r"image/demo1_greenery/pic3.png",use_container_width=True)

#endregion


#region 12. Building design & 3D modelling workflow
st.write("### 12. Building design & 3D modelling work")
building_design_expander=st.expander("Building design & 3D modelling work expander")
with building_design_expander:
    col1,col2,col3=st.columns([1.7,1.7,4])
    with col3:
        st.image(r"image/modelling/pic1.png",use_container_width=True)
    with col2:
        st.write("Solution1")
        st.image(r"image/modelling/modelling_solution1.png")
        st.write("Solution2")
        st.image(r"image/modelling/modelling_solution2.png")
        st.write("Solution3")
        st.image(r"image/modelling/modelling_solution3.png")
    with col1:
        st.write("wireframe")
        st.image(r"image/modelling/pic2.png",use_container_width=True)
    pass



#endregion

#region 13. Sensor Layout
st.write("### 13. Sensor Layout")
sensor_layout_expander=st.expander("Sensor Layout Expander")
with sensor_layout_expander:
    col1,col2=st.columns([1,1])
    with col1:
        st.image(r"image/modelling/sensor1.png",use_container_width=True)
    with col2:
        st.image(r"image/modelling/sensor2.png",use_container_width=True)
#endregion




#region Result
st.write("### Result 3D ")
col1,col2,col3=st.columns([1,1,1])
with col1:
    result_expander_demo1_solution1=st.expander("demo1_solution1")
    with result_expander_demo1_solution1:
        st.write("### demo1_solution1")
        st.image(r"image/qrcode/qr_code_demo1_solution1.png",width=150)
        url="https://app.speckle.systems/projects/c3c82e786c/models/79ad515017"
        embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"

        components.html(
            f"""
        <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
            """, 
        height=600  # Set the height explicitly for the component
        )
with col2:
    result_expander_demo1_solution2=st.expander("demo1_solution2")
    with result_expander_demo1_solution2:
        st.write("### demo1_solution2")
        st.image(r"image/qrcode/qr_code_demo1_solution2.png",width=150)
        url="https://app.speckle.systems/projects/c3c82e786c/models/8fb758d28d"
        embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"
    
        components.html(
        f"""
    <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
        """, 
    height=600  # Set the height explicitly for the component
    )
with col3:
    result_expander_demo1_solution3=st.expander("demo1_solution3")
    with result_expander_demo1_solution3:
        st.write("### demo1_solution3")
        st.image(r"image/qrcode/qr_code_demo1_solution3.png",width=150)
        url="https://app.speckle.systems/projects/c3c82e786c/models/9a3f990368"
        embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"
        
        components.html(
            f"""
        <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
            """, 
        height=600  # Set the height explicitly for the component
        )
    


print("finished")

#endregion
