import rhinoscriptsyntax as rs
import math

#region function
def getLayerByName(layerName):
    layers=rs.LayerNames()
    for i in layers:
        if i==layerName:
            return i
    return None

def get_all_objects_under_layer(layerName):
    layer_objects = rs.ObjectsByLayer(layerName)
    return layer_objects
def equalDistancePointOnCurve(curve,distance,reserveBool=False,returnPoints=True):
    if reserveBool:
        rs.ReverseCurve(curve)
    temp=[]
    ptlist=rs.DivideCurveEquidistant(curve,distance,True,returnPoints)
    # for pt in ptlist:
    #     temp.append(pt)  
    temp.extend(ptlist)
    endpt=rs.CurveEndPoint(curve)
    distance= rs.Distance(ptlist[len(ptlist)-1],endpt)  
    if round(distance,5)!=0 :
        temp.append(endpt)
        rs.AddPoint(endpt)
    return temp
def create_surface_normal_plane_by_pt(surface,pt, bool_if_create_plane_surface=False):
    param = rs.SurfaceClosestPoint(surface, pt)
    normal=rs.SurfaceNormal(surface,param)
    plane=rs.PlaneFromNormal(pt,normal)
    if bool_if_create_plane_surface:
        rs.AddPlaneSurface(plane,500,500)
    return plane
def create_hexagonal_edge_6_by_center_pt(workplane, centerPt, startPt, radius=1000):
    """Create a hexagon on a specified workplane using center point and starting point"""
    # Set the workplane
    rs.ViewCPlane(None, workplane)
    
    # Project the start point onto the workplane
    # Get workplane normal
    normal = workplane.ZAxis
    # Create vector from center to start point
    vector = rs.VectorCreate(startPt, centerPt)
    # Project vector onto workplane
    projectedVector = rs.VectorSubtract(vector, rs.VectorScale(normal, rs.VectorDotProduct(vector, normal)))
    # Create projected point
    projectedPt = rs.PointAdd(centerPt, projectedVector)
    
    # Create a new point at fixed distance from center
    unitVector = rs.VectorUnitize(projectedVector)
    firstPt = rs.PointAdd(centerPt, rs.VectorScale(unitVector, radius))
    
    # Generate hexagon points
    points = []
    for i in range(6):
        # Calculate each point by rotating around center
        pt = rs.RotateObject(firstPt, centerPt, 60*i, axis=None, copy=True)
        points.append(rs.PointCoordinates(pt))
        rs.DeleteObject(pt)
    
    # Create the hexagon polyline
    hexagon = rs.AddPolyline(points + [points[0]])
    return hexagon
def create_equilateral_triangle_up(workplane, centerPt, startPt, radius=1000):
    """Create a hexagon on a specified workplane using center point and starting point"""
    # Set the workplane
    rs.ViewCPlane(None, workplane)
    
    # Project the start point onto the workplane
    # Get workplane normal
    normal = workplane.ZAxis
    # Create vector from center to start point
    vector = rs.VectorCreate(startPt, centerPt)
    # Project vector onto workplane
    projectedVector = rs.VectorSubtract(vector, rs.VectorScale(normal, rs.VectorDotProduct(vector, normal)))
    # Create projected point
    projectedPt = rs.PointAdd(centerPt, projectedVector)
    
    # Create a new point at fixed distance from center
    unitVector = rs.VectorUnitize(projectedVector)
    firstPt = rs.PointAdd(centerPt, rs.VectorScale(unitVector, radius))
    
    # Generate hexagon points
    points = []
    for i in range(6):
        # Calculate each point by rotating around center
        pt = rs.RotateObject(firstPt, centerPt, 60*i, axis=None, copy=True)
        points.append(rs.PointCoordinates(pt))
        rs.DeleteObject(pt)
    trianglepts=[centerPt,points[1],points[2],centerPt]
    # Create the hexagon polyline
    hexagon = rs.AddPolyline(trianglepts)
    return hexagon
def create_equilateral_triangle_bottom(workplane, centerPt, startPt, radius=1000):
    """Create a hexagon on a specified workplane using center point and starting point"""
    # Set the workplane
    rs.ViewCPlane(None, workplane)
    
    # Project the start point onto the workplane
    # Get workplane normal
    normal = workplane.ZAxis
    # Create vector from center to start point
    vector = rs.VectorCreate(startPt, centerPt)
    # Project vector onto workplane
    projectedVector = rs.VectorSubtract(vector, rs.VectorScale(normal, rs.VectorDotProduct(vector, normal)))
    # Create projected point
    projectedPt = rs.PointAdd(centerPt, projectedVector)
    
    # Create a new point at fixed distance from center
    unitVector = rs.VectorUnitize(projectedVector)
    firstPt = rs.PointAdd(centerPt, rs.VectorScale(unitVector, radius))
    
    # Generate hexagon points
    points = []
    for i in range(6):
        # Calculate each point by rotating around center
        pt = rs.RotateObject(firstPt, centerPt, 60*i, axis=None, copy=True)
        points.append(rs.PointCoordinates(pt))
        rs.DeleteObject(pt)
    trianglepts=[centerPt,points[4],points[5],centerPt]
    # Create the hexagon polyline
    hexagon = rs.AddPolyline(trianglepts)
    return hexagon
def get_plane_normal(plane):
    return plane.ZAxis
def create_Normal_Line(plane,pt,length=1000):
    normal=get_plane_normal(plane)
    scaled_normal = rs.VectorScale(normal, length)
    normal_line = rs.AddLine(pt, rs.PointAdd(pt, scaled_normal))
    return normal_line      
# def create_surface_normal_plane_by_pt(surface,pt, bool_if_create_plane_surface=False):
#     param = rs.SurfaceClosestPoint(surface, pt)
#     normal=rs.SurfaceNormal(surface,param)
#     plane=rs.PlaneFromNormal(pt,normal)
#     if bool_if_create_plane_surface:
#         rs.AddPlaneSurface(plane,500,500)
#     return plane

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
                ptlist=equalDistancePointOnCurve(tempcurve,h_distance,False)
                for n in range(len(ptlist)):
                    pt_index=2*n+1

                    if pt_index<len(ptlist):
                        plane=create_surface_normal_plane_by_pt(surf,ptlist[pt_index],False)
                        rs.ViewCPlane(None, plane)  # Set the current view's construction plane
                        if rs.Distance(ptlist[pt_index],ptlist[pt_index-1])>h_distance-300:
                            if pt_index<len(ptlist)-2:
                                hexagon=create_hexagonal_edge_6_by_center_pt(plane,ptlist[pt_index],ptlist[pt_index-1],h_distance)
                                surface=rs.AddPlanarSrf(hexagon)
                                rs.ObjectLayer(surface,glass_layer)
                                rs.ObjectName(surface,"glass")
                                print(rs.ObjectName(surface))
                                if n==0:
                                    triangle_workplane=create_surface_normal_plane_by_pt(surface,ptlist[0],False)
                                    rs.ViewCPlane(None, triangle_workplane) 
                                    triangle_crv1= create_equilateral_triangle_up(triangle_workplane,ptlist[0],ptlist[1],h_distance)
                                    triangle_crv2= create_equilateral_triangle_bottom(triangle_workplane,ptlist[0],ptlist[1],h_distance)
                                    tri_srf1 = rs.AddPlanarSrf(triangle_crv1)
                                    tri_srf2 = rs.AddPlanarSrf(triangle_crv2)
                                    rs.ObjectLayer(tri_srf1,panel_layer)
                                    rs.ObjectLayer(tri_srf2,panel_layer)
                                    rs.SurfaceNormal(tri_srf1,ptlist[pt_index+1])
                                    normal_line1 = create_Normal_Line(triangle_workplane,ptlist[pt_index+1],thickness)
                                    normal_line2 = create_Normal_Line(triangle_workplane,ptlist[pt_index+1],-thickness)
                                    
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
                                    
                                triangle_workplane=create_surface_normal_plane_by_pt(surface,ptlist[pt_index+1],False)
                                rs.ViewCPlane(None, triangle_workplane) 
                                triangle_crv1= create_equilateral_triangle_up(triangle_workplane,ptlist[pt_index+1],ptlist[pt_index],h_distance)
                                triangle_crv2= create_equilateral_triangle_bottom(triangle_workplane,ptlist[pt_index+1],ptlist[pt_index],h_distance)
                                tri_srf1 = rs.AddPlanarSrf(triangle_crv1)
                                tri_srf2 = rs.AddPlanarSrf(triangle_crv2)
                                rs.ObjectLayer(tri_srf1,panel_layer)
                                rs.ObjectLayer(tri_srf2,panel_layer)
                                rs.SurfaceNormal(tri_srf1,ptlist[pt_index+1])
                                
                                normal_line1 = create_Normal_Line(triangle_workplane,ptlist[pt_index+1],thickness)
                                normal_line2 = create_Normal_Line(triangle_workplane,ptlist[pt_index+1],-thickness)
                                
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


#endregion

path=r'C:\Andy\Andy_Collection\AndyZMQ_Personal\2025_Automation\Master_Challenge\temp_surfaces.igs'
command='-Import {} _Enter _Enter'.format(path)

objs=get_all_objects_under_layer("IGES level 10000")
rs.DeleteObjects(objs)

rs.Command(command)
objs=get_all_objects_under_layer("IGES level 10000")

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


h_distance=5000 
thickness=300
v_distance=h_distance*(math.sqrt(3)/2)

result1_layer=getLayerByName("result1")
result2_layer=getLayerByName("result2")
glass1_layer=getLayerByName("glass1")
glass2_layer=getLayerByName("glass2")
panel1_layer=getLayerByName("panel1")
panel2_layer=getLayerByName("panel2")
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












