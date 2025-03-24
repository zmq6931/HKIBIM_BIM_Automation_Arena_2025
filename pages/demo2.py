import streamlit as st
import pythoncom
try:
    import adfun as adfun
except:
    from importlib.machinery import SourceFileLoader
    adfun = SourceFileLoader("module.name",r"adfun.py").load_module()
import array
import math
from streamlit.components.v1 import iframe
import streamlit.components.v1 as components

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
    col1,col2,col3=st.columns(3)
    with col1:
        input_Width = st.number_input("Width",min_value=40000,value=47000,step=100)
    with col2:
        input_Length = st.number_input("Length", min_value=60000,value=69800,step=100)
    with col3:
        input_Height = st.number_input("Height",min_value=13000,value=18000,step=50)
    btn_change_parameter=st.button("Change Parameter",use_container_width=True)
    pythoncom.CoInitialize()

    if btn_change_parameter:
        dp=adfun.mydpfun.getDpApplication()
        doc=dp.ActiveDocument
        osel=doc.Selection
        part=doc.Part
        hsf=part.HybridShapeFactory
        parameters=part.Parameters
        width=parameters["Width"]
        length=parameters["Length"]
        height=parameters["Height"]
        resultGeo=part.HybridBodies.item("ResultGeo")
        curveGeo=part.HybridBodies.item("curves")

        dp.DisplayFileAlerts=False
        st.write("Width: ",input_Width,"Length: ",input_Length,"Height: ",input_Height)

        width.Value=input_Width
        length.Value=input_Length
        height.Value=input_Height
        
        part.Update()
    btn_saveas_iges=st.button("Save as IGES",use_container_width=True)
    if btn_saveas_iges:
        dp=adfun.mydpfun.getDpApplication()
        doc=dp.ActiveDocument
        st.write("Saving as IGES...")
        export_path=r"C:\Andy\Andy_Collection\AndyZMQ_Personal\2025_Automation\Master_Challenge\temp_surfaces.igs"
        name=export_path.split('.')[0]
        format=export_path.split('.')[1]
        doc.ExportData(name,format)

   
st.divider()
st.write("### Step 2 panel automation")
col1,col2=st.columns([0.8,1.1])
with col1:
    step2_expander=st.expander("Step 2 panel automation")
    with step2_expander:
        st.write("### Step 2 panel automation")
        st.video(r"image\deom2\rhino_panel_generation.mp4")
with col2:
    step2_code_expander=st.expander("Step 2 panel automation python code")
    with step2_code_expander:        
        code=r"""
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
                            

create_panel_and_glass1(crv1,surf1,glass1_layer,panel1_layer)

surf2_layer_objects = rs.ObjectsByLayer("surf2")
crv2=[obj for obj in surf2_layer_objects if rs.IsCurve(obj)][0]
surf2=[obj for obj in surf2_layer_objects if rs.IsSurface(obj)][0]

rs.CurrentLayer(result2_layer)

create_panel_and_glass1(crv2,surf2,glass2_layer,panel2_layer)


rs.CurrentLayer("templayer")

rs.LayerVisible("result1",False)
rs.LayerVisible("result2",False)


print("finished")


        """
        
        # st.markdown(f'<div class="code-container"><pre><code>{code}</code></pre></div>', unsafe_allow_html=True)
        code_container= st.container(height=400,border=False)
        with code_container:
            st.code(code, language='python',wrap_lines=False)


st.divider()

st.write("### Step 3 steel frames automation")
step3_transom_expander=st.expander("Step 3 steel frames automation")
with step3_transom_expander:
    st.video(r"image/deom2/rhino_tekla_transom.mp4",format="video/mp4")

    col1,col2=st.columns([2.5,1])
    with col1:
        cola,colb=st.columns([1.3,1])
        with cola:
            st.image(r"image/deom2/grasshopper_image.png")
        with colb:
            st.image(r"image/deom2/tekla_command.png")
    with col2:
        st.write("### Tekla - Grasshopper plugin code")
        code_container=st.container(height=700,border=True)
        code="""
using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using System.Windows.Forms;
using TSM = Tekla.Structures.Model;
using TSG = Tekla.Structures.Geometry3d;
using tkfun = Tekla_Demo.TeklaFun;
using System.Linq;
using TSMUI=Tekla.Structures.Model.UI;




namespace HKIBIM_Automation_2025_Demo2
{
    public class HKIBIM_Automation_2025_DemoComponent2 : GH_Component
    {
        #region Properties
        bool isConnectToTekla=false;
        TSM.Model model = null;

        List<int> beamlist =new List<int>();

        #endregion



        /// <summary>
        /// Each implementation of GH_Component must provide a public 
        /// constructor without any arguments.
        /// Category represents the Tab in which the component will appear, 
        /// Subcategory the panel. If you use non-existing tab or panel names, 
        /// new tabs/panels will automatically be created.
        /// </summary>
        public HKIBIM_Automation_2025_DemoComponent2()
          : base("transom generation", "Andy",//HKIBIM_Automation_2025_Demo2Component
            "transom generation",
            "HKIBIM_Automation_2025_Demo2", "transom")
        {
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Profile", "P", "tekla beam Profile", GH_ParamAccess.item, "D100");
            pManager.AddLineParameter("Line", "L", "line", GH_ParamAccess.list);
            //pManager.AddBooleanParameter("Run","R","Run",GH_ParamAccess.item,false);

        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            // Use the pManager object to register your output parameters.
            // Output parameters do not have default values, but they too must have the correct access type.

            //pManager.AddCurveParameter("Spiral", "S", "Spiral curve", GH_ParamAccess.item);
            
            // Sometimes you want to hide a specific parameter from the Rhino preview.
            // You can use the HideParameter() method as a quick way:
            //pManager.HideParameter(0);
        }

        protected override void AfterSolveInstance()
        {


        }
        protected override void BeforeSolveInstance()
        {
            model = new TSM.Model();

            isConnectToTekla = model.GetConnectionStatus();


            if (isConnectToTekla == false)
            {
                MessageBox.Show("Tekla is not connected. Connection status: " + model.GetConnectionStatus().ToString());

            }

            var objs = model.GetModelObjectSelector().GetAllObjects();

            while (objs.MoveNext())
            {
                TSM.Beam b = objs.Current as TSM.Beam;
                if (b != null)
                {
                    if (beamlist.Where(x => x == b.Identifier.ID).Count() != 0)
                    {
                        beamlist.Remove(b.Identifier.ID);
                        b.Delete();

                        //MessageBox.Show("ff");
                    }
                }
            }
            model.CommitChanges();


            


        }

        

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            string profile = "D100";
            bool bool_run = false;
            List<Line> lines = new List<Line>();

            //Line line=new Line();


            if (!DA.GetData(0, ref profile)) return;
            if (!DA.GetDataList(1, lines)) return;
            //if (!DA.GetData(2, ref bool_run)) return;


            try
            {

                foreach (Line l in lines)
                {
                    Point3d pt1 = l.PointAt(0);
                    Point3d pt2 = l.PointAt(1);

                    TSG.Point tk_pt1 = new TSG.Point(pt1.X, pt1.Y, pt1.Z);
                    TSG.Point tk_pt2 = new TSG.Point(pt2.X, pt2.Y, pt2.Z);

                    var beam = tkfun.BeamCreatePtPt(tk_pt1, tk_pt2, profile);
                    beamlist.Add(beam.Identifier.ID);

                }
            }
            catch (Exception)
            {
            }

            model.CommitChanges();

        }

        Curve CreateSpiral(Plane plane, double r0, double r1, Int32 turns)
        {
            Line l0 = new Line(plane.Origin + r0 * plane.XAxis, plane.Origin + r1 * plane.XAxis);
            Line l1 = new Line(plane.Origin - r0 * plane.XAxis, plane.Origin - r1 * plane.XAxis);

            Point3d[] p0;
            Point3d[] p1;

            l0.ToNurbsCurve().DivideByCount(turns, true, out p0);
            l1.ToNurbsCurve().DivideByCount(turns, true, out p1);

            PolyCurve spiral = new PolyCurve();

            for (int i = 0; i < p0.Length - 1; i++)
            {
                Arc arc0 = new Arc(p0[i], plane.YAxis, p1[i + 1]);
                Arc arc1 = new Arc(p1[i + 1], -plane.YAxis, p0[i + 1]);

                spiral.Append(arc0);
                spiral.Append(arc1);
            }

            return spiral;
        }

        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.primary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => null;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("5c7e40c2-cc64-4563-9cfa-254a3b59e3d6");
    }
}        
        """
        with code_container:
            st.code(code, language='c#',wrap_lines=True)


st.divider()
st.write("### step 4 Drawing Generation")
btn_drawing_generation=st.button("Drawing Generation",use_container_width=True)
pythoncom.CoInitialize()

if btn_drawing_generation:
    app=adfun.mycadfun.getAutocadApp()
    doc=adfun.mycadfun.getActiveDocument(app)
    modelSpace=adfun.mycadfun.getModelSpace(doc)

    # Create hexagon with side length 2500
    hex_side = 2500
    hex_pts = [
        array.array('d', [0, 0, 0]),
        array.array('d', [hex_side, 0, 0]),
        array.array('d', [1.5*hex_side, -hex_side*math.sqrt(3)/2, 0]),
        array.array('d', [hex_side, -hex_side*math.sqrt(3), 0]),
        array.array('d', [0, -hex_side*math.sqrt(3), 0]),
        array.array('d', [-0.5*hex_side, -hex_side*math.sqrt(3)/2, 0])
    ]
    
    # Draw hexagon lines
    for i in range(len(hex_pts)):
        start = hex_pts[i]
        end = hex_pts[(i+1)%len(hex_pts)]
        modelSpace.AddLine(start, end)
        dimension1= adfun.mycadfun.dimensionPtPt(modelSpace,start,end,array.array('d',[(start[0]+end[0])/2,(start[1]+end[1])/2+220,(start[2]+end[2])/2]))   

    adfun.mycadfun.dimension3PointAngular(modelSpace,hex_pts[3], hex_pts[2], hex_pts[4],
                                          array.array('d', [hex_pts[3][0]+200, hex_pts[3][1]+600, 0]), 100)
    tri_side = 2500
    tri_start = array.array('d', [0, -3*hex_side , 0])
    tri_pts = [
        tri_start,
        array.array('d', [tri_side, -3*hex_side, 0]),
        array.array('d', [tri_side/2, -3*hex_side + tri_side*math.sqrt(3)/2, 0])
    ]
    
    # Draw triangle lines
    for i in range(len(tri_pts)):
        start = tri_pts[i]
        end = tri_pts[(i+1)%len(tri_pts)]
        modelSpace.AddLine(start, end)
        dimension1= adfun.mycadfun.dimensionPtPt(modelSpace,start,end,array.array('d',[(start[0]+end[0])/2,(start[1]+end[1])/2+220,(start[2]+end[2])/2]))   
    

     


    adfun.mycadfun.dimension3PointAngular(modelSpace,tri_pts[0], tri_pts[1], tri_pts[2],
                                          array.array('d', [tri_pts[0][0]+200, tri_pts[0][1]+200, 0]), 100)
    doc.Regen(True)

drawing_generation_expander=st.expander("Drawing Generation expander")
with drawing_generation_expander:
    col1,col2=st.columns([2,1])
    with col1:
        video_path=r"image/deom2/demo2_drawing_generation.mp4"
        v=st.video(video_path,format="video/mp4")
    with col2:
        code_container=st.container(height=400,border=False)
        with code_container:
            code=r"""
        app=adfun.mycadfun.getAutocadApp()
        doc=adfun.mycadfun.getActiveDocument(app)
        modelSpace=adfun.mycadfun.getModelSpace(doc)

        # Create hexagon with side length 2500
        hex_side = 2500
        hex_pts = [
            array.array('d', [0, 0, 0]),
            array.array('d', [hex_side, 0, 0]),
            array.array('d', [1.5*hex_side, -hex_side*math.sqrt(3)/2, 0]),
            array.array('d', [hex_side, -hex_side*math.sqrt(3), 0]),
            array.array('d', [0, -hex_side*math.sqrt(3), 0]),
            array.array('d', [-0.5*hex_side, -hex_side*math.sqrt(3)/2, 0])
        ]
        
        # Draw hexagon lines
        for i in range(len(hex_pts)):
            start = hex_pts[i]
            end = hex_pts[(i+1)%len(hex_pts)]
            modelSpace.AddLine(start, end)
            dimension1= adfun.mycadfun.dimensionPtPt(modelSpace,start,end,array.array('d',[(start[0]+end[0])/2,(start[1]+end[1])/2+220,(start[2]+end[2])/2]))   

        adfun.mycadfun.dimension3PointAngular(modelSpace,hex_pts[3], hex_pts[2], hex_pts[4],
                                            array.array('d', [hex_pts[3][0]+200, hex_pts[3][1]+600, 0]), 100)
        tri_side = 2500
        tri_start = array.array('d', [0, -9000 , 0])
        tri_pts = [
            tri_start,
            array.array('d', [tri_side, -9000, 0]),
            array.array('d', [tri_side/2, -9000 + tri_side*math.sqrt(3)/2, 0])
        ]
        
        # Draw triangle lines
        for i in range(len(tri_pts)):
            start = tri_pts[i]
            end = tri_pts[(i+1)%len(tri_pts)]
            modelSpace.AddLine(start, end)
            dimension1= adfun.mycadfun.dimensionPtPt(modelSpace,start,end,array.array('d',[(start[0]+end[0])/2,(start[1]+end[1])/2+220,(start[2]+end[2])/2]))   
        

        


        adfun.mycadfun.dimension3PointAngular(modelSpace,tri_pts[0], tri_pts[1], tri_pts[2],
                                            array.array('d', [tri_pts[0][0]+200, tri_pts[0][1]+200, 0]), 100)
        doc.Regen(True)
            
            """
            st.code(code, language='python',wrap_lines=True)

    # st.components.v1.html(f'<div style="height: 300px; overflow: hidden;">{st.video(video_path)}</div>', height=300)
    # st.components.v1.html(f'<div style="height: 200px; overflow: hidden;">{st.video(video_path)}</div>', height=200)  # Updated height


st.divider()
st.write("### step 5 Lighting and Greenery and 3D modelling work refer to demo1")

st.divider()
st.write("### Result 3D ")
result_expander_demo2_solution1=st.expander("demo2_solution1")
with result_expander_demo2_solution1:
    st.write("### demo2_solution1")
    st.image(r"image/qrcode/qr_code_demo2_solution1.png",width=200)
    url="https://app.speckle.systems/projects/c3c82e786c/models/13ea69d790"
    embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"

    components.html(
        f"""
    <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
        """, 
    height=600  # Set the height explicitly for the component
    )
    
result_expander_demo2_solution2=st.expander("demo2_solution2")
with result_expander_demo2_solution2:
    st.write("### demo2_solution2")
    st.image(r"image/qrcode/qr_code_demo2_solution2.png",width=200)
    url="https://app.speckle.systems/projects/c3c82e786c/models/30f0dd317a"
    embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"
    
    components.html(
        f"""
    <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
        """, 
    height=600  # Set the height explicitly for the component
    )
    
result_expander_demo2_solution3=st.expander("demo2_solution3")
with result_expander_demo2_solution3:
    st.write("### demo2_solution3")
    st.image(r"image/qrcode/qr_code_demo2_solution3.png",width=200)
    url="https://app.speckle.systems/projects/c3c82e786c/models/90eb482cbb"
    embed_url=f"{url}#embed=%7B%22isEnabled%22%3Atrue%7D"
    
    components.html(
        f"""
    <iframe title="Speckle" src="{embed_url}" style="width:100%; height:600px;" frameborder="1"></iframe>
        """, 
    height=600  # Set the height explicitly for the component
    )
    








    