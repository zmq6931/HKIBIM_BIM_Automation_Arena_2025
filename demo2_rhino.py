import rhinoscriptsyntax as rs
from rhfun import myfun as rhfun
import math


path=r'C:\Andy\Andy_Collection\AndyZMQ_Personal\2025_Automation\Master_Challenge\temp_surfaces.igs'
command='-Import {} _Enter _Enter'.format(path)

objs=rhfun.get.get_all_objects_under_layer("IGES level 10000")
rs.DeleteObjects(objs)

rs.Command(command)
objs=rhfun.get.get_all_objects_under_layer("IGES level 10000")

surf1=[x for x in objs if rs.IsSurface(x)][0]
surf2=[x for x in objs if rs.IsSurface(x)][1]

crv1=[x for x in objs if rs.IsCurve(x)][0]
crv2=[x for x in objs if rs.IsCurve(x)][1]

if rs.Area(surf1)>rs.Area(surf2):
    surf1,surf2=surf2,surf1
else:
    surf2,surf1=surf1,surf2



crv1_start = rs.CurveStartPoint(crv1)
crv1_end = rs.CurveEndPoint(crv1)

isOnSurf= rs.IsPointOnSurface(surf1,crv1_start)
if  isOnSurf:
    crv1,crv2=crv1,crv2
else:
    crv1,crv2=crv2,crv1
print(isOnSurf)

rs.ReverseCurve(crv1)
rs.ReverseCurve(crv2)


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

# surf1_layer_objects = rs.ObjectsByLayer("surf1")
# crv1=[obj for obj in surf1_layer_objects if rs.IsCurve(obj)][0]
# surf1=[obj for obj in surf1_layer_objects if rs.IsSurface(obj)][0]


def create_panel_and_glass1(offset_crv,surf,glass_layer,panel_layer,iterate_number=5,multi_index_0_or_1=0):
    for i in range(0,iterate_number):
        offset_crv1 = rs.OffsetCurveOnSurface(offset_crv, surf, -i*v_distance)
        
        if i==0:
            offset_crv1=offset_crv
        else:
            if isinstance(offset_crv1,list):
                try:
                    if multi_index_0_or_1==0:
                        offset_crv1=offset_crv1[0]
                    else:
                        offset_crv1=offset_crv1[1]
                except:
                    offset_crv1=offset_crv1[0]
                    
                    # if multi_index_0_or_1==0:
                    #     offset_crv1=offset_crv1[1]
                    # else:
                    #     offset_crv1=offset_crv1[0]
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
                                rs.ObjectName(surface,"glass")
                                print(rs.ObjectName(surface))
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
                            

create_panel_and_glass1(crv1,surf1,glass1_layer,panel1_layer,iterate_number=10,multi_index_0_or_1=0)

# surf2_layer_objects = rs.ObjectsByLayer("surf2")
# crv2=[obj for obj in surf2_layer_objects if rs.IsCurve(obj)][0]
# surf2=[obj for obj in surf2_layer_objects if rs.IsSurface(obj)][0]

rs.CurrentLayer(result2_layer)

create_panel_and_glass1(crv2,surf2,glass2_layer,panel2_layer,iterate_number=20,multi_index_0_or_1=0)


rs.CurrentLayer("templayer")

rs.LayerVisible("result1",False)
rs.LayerVisible("result2",False)




print("finished")












