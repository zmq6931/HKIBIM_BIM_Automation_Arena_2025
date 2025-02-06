import rhinoscriptsyntax as rs


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
result1_layer = rs.CurrentLayer("result1")
layer_objects = rs.ObjectsByLayer("surf1")

surf1_crv=[obj for obj in layer_objects if rs.IsCurve(obj)][0]

mid_pt=rs.CurveMidPoint(surf1_crv)


pt=rs.AddPoint(mid_pt)












