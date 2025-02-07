import rhinoscriptsyntax as rs
from rhfun import myfun as rhfun





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

# surf1_layer = rs.CurrentLayer("surf1")

result1_layer=rhfun.layer.getLayerByName("result1")
result2_layer=rhfun.layer.getLayerByName("result2")


surf1_layer_objects = rs.ObjectsByLayer("surf1")
surf1_crv=[obj for obj in surf1_layer_objects if rs.IsCurve(obj)][0]


print(rhfun.get.get_object_name(surf1_crv))

print("finished")












