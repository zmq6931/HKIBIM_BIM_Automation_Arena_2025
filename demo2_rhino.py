import rhinoscriptsyntax as rs
from rhfun import myfun as rhfun
import math




@staticmethod
def equalDistancePointOnCurve(curve,distance,reserveBool=False):
    if reserveBool:
        rs.ReverseCurve(curve)
    temp=[]
    ptlist=rs.DivideCurveEquidistant(curve,distance,True)
    # for pt in ptlist:
    #     temp.append(pt)  
    temp.extend(ptlist)
    endpt=rs.CurveEndPoint(curve)
    distance= rs.Distance(ptlist[len(ptlist)-1],endpt)  
    if round(distance,5)!=0 :
        temp.append(endpt)
        rs.AddPoint(endpt)
    return temp



h_distance=2000
gap=50
v_distance=h_distance*(math.sqrt(3)/2)


result1_layer=rhfun.layer.getLayerByName("result1")
result2_layer=rhfun.layer.getLayerByName("result2")
rs.CurrentLayer(result1_layer) # set result1 layer

objs=rs.ObjectsByLayer(result1_layer)
rs.DeleteObjects(objs)

surf1_layer_objects = rs.ObjectsByLayer("surf1")
crv1=[obj for obj in surf1_layer_objects if rs.IsCurve(obj)][0]
surf1=[obj for obj in surf1_layer_objects if rs.IsSurface(obj)][0]
rs.ReverseCurve(crv1)
ptlist=rhfun.point.equalDistancePointOnCurve(crv1,h_distance)

rs.OffsetCurveOnSurface(crv1,surf1,v_distance)

rhfun.plane.create_surface_normal_plane_by_pt(surf1,ptlist[2],False)






print("finished")












