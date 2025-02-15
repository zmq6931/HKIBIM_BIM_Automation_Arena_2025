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
col1,col2=st.columns([0.8,1.1])
with col1:
    step2_expander=st.expander("Step 2 panel automation")
    with step2_expander:
        st.write("### Step 2 panel automation")
        st.video(r"image\deom2\rhino_panel_generation.mp4")
with col2:
    step2_code_expander=st.expander("Step 2 panel automation code")
    with step2_code_expander:

        
        code="""
import rhinoscriptsyntax as rs
from rhfun import myfun as rhfun
import math

h_distance=2500
thickness=100
v_distance=h_distance*(math.sqrt(3)/2)

result1_layer=rhfun.layer.getLayerByName("result1")
result2_layer=rhfun.layer.getLayerByName("result2")
glass1_layer=rhfun.layer.getLayerByName("glass1")
glass2_layer=rhfun.layer.getLayerByName("glass2")
panel1_layer=rhfun.layer.getLayerByName("panel1")
panel2_layer=rhfun.layer.getLayerByName("panel2")
rs.CurrentLayer(result1_layer) # set result1 layer

objs=rs.ObjectsByLayer(result1_layer)
rs.DeleteObjects(objs)
objs=rs.ObjectsByLayer(result2_layer)
rs.DeleteObjects(objs)
objs=rs.ObjectsByLayer(glass1_layer)
rs.DeleteObjects(objs)
objs=rs.ObjectsByLayer(glass2_layer)
rs.DeleteObjects(objs)
objs=rs.ObjectsByLayer(panel1_layer)
rs.DeleteObjects(objs)
objs=rs.ObjectsByLayer(panel2_layer)
rs.DeleteObjects(objs)

surf1_layer_objects = rs.ObjectsByLayer("surf1")
crv1=[obj for obj in surf1_layer_objects if rs.IsCurve(obj)][0]
surf1=[obj for obj in surf1_layer_objects if rs.IsSurface(obj)][0]


def export_to_iges(fullpath):
    # rs.Command("-_Export",True)
    rs.UnselectAllObjects()
    rs.SelectObjects(rs.AllObjects())

    
    fileFullPath = " \""+fullpath+"\""
    # command = +fileFullPath+" Enter"
    command = "-_Export "+fileFullPath+" Enter"
    
    # Execute the export command
    rs.Command(command, True)
    

def create_panel_and_glass1(offset_crv,surf,glass_layer,panel_layer):
    for i in range(0,50):
        offset_crv1 = rs.OffsetCurveOnSurface(offset_crv, surf, -i*v_distance)
        
        if i==0:
            offset_crv1=offset_crv
        else:
            if isinstance(offset_crv1,list):
                try:
                    offset_crv1=offset_crv1[1]
                except:
                    offset_crv1=offset_crv1[0]
            else:
                offset_crv1=offset_crv1
        if offset_crv1 != None:
            print(offset_crv1)
            
            tempcurve=rs.coercecurve(offset_crv1)    
            
            if i%2==0:
                ptlist=rhfun.point.equalDistancePointOnCurve(tempcurve,h_distance,False)
                for n in range(len(ptlist)):
                    pt_index=2*n+1

                    if pt_index<len(ptlist):
                        plane=rhfun.plane.create_surface_normal_plane_by_pt(surf,ptlist[pt_index],False)
                        rs.ViewCPlane(None, plane)  # Set the current view's construction plane
                        if rs.Distance(ptlist[pt_index],ptlist[pt_index-1])>h_distance-300:
                            if pt_index<len(ptlist)-2:
                                hexagon=rhfun.hexagon.create_hexagonal_edge_6_by_center_pt(plane,ptlist[pt_index],ptlist[pt_index-1],h_distance)
                                surface=rs.AddPlanarSrf(hexagon)
                                rs.ObjectLayer(surface,glass_layer)
                                if n==0:
                                    triangle_workplane=rhfun.plane.create_surface_normal_plane_by_pt(surface,ptlist[0],False)
                                    rs.ViewCPlane(None, triangle_workplane) 
                                    triangle_crv1= rhfun.hexagon.create_equilateral_triangle_up(triangle_workplane,ptlist[0],ptlist[1],h_distance)
                                    triangle_crv2= rhfun.hexagon.create_equilateral_triangle_bottom(triangle_workplane,ptlist[0],ptlist[1],h_distance)
                                    tri_srf1 = rs.AddPlanarSrf(triangle_crv1)
                                    tri_srf2 = rs.AddPlanarSrf(triangle_crv2)
                                    rs.ObjectLayer(tri_srf1,panel_layer)
                                    rs.ObjectLayer(tri_srf2,panel_layer)
                                    rs.SurfaceNormal(tri_srf1,ptlist[pt_index+1])
                                    normal_line1 = rhfun.line.create_Normal_Line(triangle_workplane,ptlist[pt_index+1],300)
                                    normal_line2 = rhfun.line.create_Normal_Line(triangle_workplane,ptlist[pt_index+1],-300)
                                    
                                    # Extrude triangle surfaces
                                    extruded_tri1 = rs.ExtrudeSurface(tri_srf1, normal_line1)
                                    extruded_tri2 = rs.ExtrudeSurface(tri_srf2, normal_line1)
                                    extruded_tri3 = rs.ExtrudeSurface(tri_srf1, normal_line2)
                                    extruded_tri4 = rs.ExtrudeSurface(tri_srf2, normal_line2)
                                    rs.ObjectLayer(extruded_tri1,panel_layer)
                                    rs.ObjectLayer(extruded_tri2,panel_layer)
                                    rs.ObjectLayer(extruded_tri3,panel_layer)
                                    rs.ObjectLayer(extruded_tri4,panel_layer)
                                    rs.DeleteObjects(normal_line1)
                                    rs.DeleteObjects(normal_line2)
                                    
                                triangle_workplane=rhfun.plane.create_surface_normal_plane_by_pt(surface,ptlist[pt_index+1],False)
                                rs.ViewCPlane(None, triangle_workplane) 
                                triangle_crv1= rhfun.hexagon.create_equilateral_triangle_up(triangle_workplane,ptlist[pt_index+1],ptlist[pt_index],h_distance)
                                triangle_crv2= rhfun.hexagon.create_equilateral_triangle_bottom(triangle_workplane,ptlist[pt_index+1],ptlist[pt_index],h_distance)
                                tri_srf1 = rs.AddPlanarSrf(triangle_crv1)
                                tri_srf2 = rs.AddPlanarSrf(triangle_crv2)
                                rs.ObjectLayer(tri_srf1,panel_layer)
                                rs.ObjectLayer(tri_srf2,panel_layer)
                                rs.SurfaceNormal(tri_srf1,ptlist[pt_index+1])
                                
                                normal_line1 = rhfun.line.create_Normal_Line(triangle_workplane,ptlist[pt_index+1],300)
                                normal_line2 = rhfun.line.create_Normal_Line(triangle_workplane,ptlist[pt_index+1],-300)
                                
                                # Extrude triangle surfaces
                                extruded_tri1 = rs.ExtrudeSurface(tri_srf1, normal_line1)
                                extruded_tri2 = rs.ExtrudeSurface(tri_srf2, normal_line1)
                                extruded_tri3 = rs.ExtrudeSurface(tri_srf1, normal_line2)
                                extruded_tri4 = rs.ExtrudeSurface(tri_srf2, normal_line2)
                                rs.ObjectLayer(extruded_tri1,panel_layer)
                                rs.ObjectLayer(extruded_tri2,panel_layer)
                                rs.ObjectLayer(extruded_tri3,panel_layer)
                                rs.ObjectLayer(extruded_tri4,panel_layer)
                                rs.DeleteObjects(normal_line1)
                                rs.DeleteObjects(normal_line2)
                            

surf2_layer_objects = rs.ObjectsByLayer("surf2")
crv2=[obj for obj in surf2_layer_objects if rs.IsCurve(obj)][0]
surf2=[obj for obj in surf2_layer_objects if rs.IsSurface(obj)][0]

rs.CurrentLayer(result2_layer)

export_to_iges(r"C:\Andy\Andy_Collection\AndyZMQ_Personal\2025_Automation\Master_Challenge\demo2_panel.igs")


print("finished")




        """
        
        # st.markdown(f'<div class="code-container"><pre><code>{code}</code></pre></div>', unsafe_allow_html=True)
        code_container= st.container(height=400,border=False)
        with code_container:
            st.code(code, language='python',wrap_lines=False)


# st.container(
#     st.code(code,language="python"),height=1200,border=2
# )













    