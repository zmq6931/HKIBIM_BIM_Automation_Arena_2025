
import pandas as pd
import numpy as np
import win32com.client
import comtypes.client
import array

class mydpfun(object):
    @staticmethod
    def call_catscript_or_catvbs(dp,catscript_folder=r"C:\Andy\pycode\Andy_Python\CATScript",CATScript_fileName="adfun_catia.catvbs",functionName="CATMain",parameters=None,CatScriptLibraryType =1):
        '''
        CatScriptLibraryType =1 is catScriptLibraryTypeDirectory
        functionName="CATMain" or use functionName like PointsOnCurveInsertedByPointDistance
        parameters=[osel,hsf,geo,curve,1000,True,-1], if function has input parameters, then use array to pass parameter
        
        example: call_catscript_or_catvbs(
            dp,catscript_folder=r"C:\Andy\pycode\Andy_Python\CATScript", 
            CATScript_fileName="adfun_catia.catvbs",
            functionName="PointsOnCurveInsertedByPointDistance",
            parameters=[osel,hsf,geo,curve,1000,True,-1],
            CatScriptLibraryType =1)
        '''
        ss=dp.SystemService

        ss.ExecuteScript(catscript_folder, CatScriptLibraryType, CATScript_fileName, functionName, parameters);


    @staticmethod
    def hideCurrentSelection(osel):
        visPropertyset = osel.VisProperties;
        # osel.Clear();
        # osel.Add(obj);
        visPropertyset.SetShow(1);
        osel.Clear();
    @staticmethod
    def hideElementlist(osel,objlist):    
        visPropertyset = osel.VisProperties;
        osel.Clear();
        for i in objlist:
            osel.Add(i);
        visPropertyset.SetShow(1);
        osel.Clear();
    @staticmethod
    def showElement(osel,obj):
        visPropertyset = osel.VisProperties;
        osel.Clear();
        osel.Add(obj);
        visPropertyset.SetShow(0);
        osel.Clear();
    @staticmethod
    def hideElement(osel,obj):
        visPropertyset = osel.VisProperties
        osel.Clear()
        osel.Add(obj)
        visPropertyset.SetShow(1)
        osel.Clear()
    @staticmethod
    def add_new_window(catiaOrDp,number=1):
        # dp = win32com.client.Dispatch("digitalproject.application")
        doc = catiaOrDp.activedocument
        windows = []
        for i in range(0, number):
            windows.append(doc.newwindow())
        print("finish add windows")
        # return number
        return windows

    @staticmethod
    def getDpApplication():
        dp = win32com.client.dynamic.Dispatch("digitalproject.application")
        return dp
    @staticmethod
    def getCatiaApplication():
        dp = win32com.client.Dispatch("catia.application")
        return dp
    @staticmethod
    def getTypeName(catia, obj):
        code = '''
        Function mytypename(obj) 
        temp=TypeName(obj)
        mytypename=temp
        End Function'''
        ss = catia.systemService
        para = []
        para.append(obj)
        typename = ss.Evaluate(code, 0, "mytypename", para)
        return typename

    @staticmethod
    def partDefinedByObject(element):
        part = None
        ispart = False
        while (not ispart):
            if (mydpfun.getTypeName(element) != "Part"):
                element = element.parent
                continue
            part = element
            ispart = True
        return part

    @staticmethod
    def getisUpdateBool(part, AnyObject):
        return part.isuptodate(AnyObject)

    class powerCopy(object):
        @staticmethod
        def part_pc_inputElement1(part, resultGeo, pcname, pcpath, inputname1, inputobject1, updatebool=False):
            # dp = win32com.client.Dispatch("digitalproject.application")
            # part = dp.activedocument.part
            # Get InstanceFactory
            part.inworkobject = resultGeo
            instanceFactory = part.GetCustomerFactory("InstanceFactory")
            instanceFactory.BeginInstanceFactory(pcname, pcpath)
            instanceFactory.BeginInstantiate()
            # define input
            instanceFactory.PutInputData(inputname1, inputobject1)
            # instanceFactory.GetParameter("radius").valuatefromstring("50mm")   #define parameter
            # instantiate
            instanceFactory.Instantiate()
            # end InstanceFactory
            instanceFactory.EndInstantiate()
            instanceFactory.EndInstanceFactory()
            if updatebool == True: part.updateobject(instanceFactory)

        @staticmethod
        def part_pc_inputElement2(part, resultGeo, pcname, pcpath, inputname1, inputobject1,
                                  inputname2, inputobject2, updatebool=False):
            part.inworkobject = resultGeo
            # Get InstanceFactory
            instanceFactory = part.GetCustomerFactory("InstanceFactory")
            instanceFactory.BeginInstanceFactory(pcname, pcpath)
            instanceFactory.BeginInstantiate()
            # define input
            instanceFactory.PutInputData(inputname1, inputobject1)
            instanceFactory.PutInputData(inputname2, inputobject2)
            # instanceFactory.GetParameter("radius").valuatefromstring("50mm")   #define parameter
            # instantiate
            instanceFactory.Instantiate()
            # end InstanceFactory
            instanceFactory.EndInstantiate()
            instanceFactory.EndInstanceFactory()
            if updatebool == True: part.updateobject(instanceFactory)

        @staticmethod
        def part_pc_inputElement3(part, resultGeo, pcname, pcpath, inputname1, inputobject1,
                                  inputname2, inputobject2, inputname3, inputobject3, updatebool=False):
            part.inworkobject = resultGeo
            # Get InstanceFactory
            instanceFactory = part.GetCustomerFactory("InstanceFactory")
            instanceFactory.BeginInstanceFactory(pcname, pcpath)
            instanceFactory.BeginInstantiate()
            # define input
            instanceFactory.PutInputData(inputname1, inputobject1)
            instanceFactory.PutInputData(inputname2, inputobject2)
            instanceFactory.PutInputData(inputname3, inputobject3)
            # instanceFactory.GetParameter("radius").valuatefromstring("50mm")   #define parameter
            # instantiate
            instanceFactory.Instantiate()
            # end InstanceFactory
            instanceFactory.EndInstantiate()
            instanceFactory.EndInstanceFactory()
            if updatebool == True: part.updateobject(instanceFactory)

        @staticmethod
        def part_pc_inputElement4(part, resultGeo, pcname, pcpath, inputname1, inputobject1,
                                  inputname2, inputobject2, inputname3,
                                  inputobject3, inputname4, inputobject4, updatebool=False):
            part.inworkobject = resultGeo
            # Get InstanceFactory
            instanceFactory = part.GetCustomerFactory("InstanceFactory")
            instanceFactory.BeginInstanceFactory(pcname, pcpath)
            instanceFactory.BeginInstantiate()
            # define input
            instanceFactory.PutInputData(inputname1, inputobject1)
            instanceFactory.PutInputData(inputname2, inputobject2)
            instanceFactory.PutInputData(inputname3, inputobject3)
            instanceFactory.PutInputData(inputname4, inputobject4)

            # instanceFactory.GetParameter("radius").valuatefromstring("50mm")   #define parameter
            # instantiate
            instanceFactory.Instantiate()
            # end InstanceFactory
            instanceFactory.EndInstantiate()
            instanceFactory.EndInstanceFactory()
            if updatebool == True: part.updateobject(instanceFactory)

        @staticmethod
        def part_pc_inputElement5(part, resultGeo, pcname, pcpath, inputname1, inputobject1,
                                  inputname2, inputobject2, inputname3,
                                  inputobject3, inputname4, inputobject4,
                                  inputname5, inputobject5, updatebool=False):
            part.inworkobject = resultGeo
            # Get InstanceFactory
            instanceFactory = part.GetCustomerFactory("InstanceFactory")
            instanceFactory.BeginInstanceFactory(pcname, pcpath)
            instanceFactory.BeginInstantiate()
            # define input
            instanceFactory.PutInputData(inputname1, inputobject1)
            instanceFactory.PutInputData(inputname2, inputobject2)
            instanceFactory.PutInputData(inputname3, inputobject3)
            instanceFactory.PutInputData(inputname4, inputobject4)
            instanceFactory.PutInputData(inputname5, inputobject5)

            # instanceFactory.GetParameter("radius").valuatefromstring("50mm")   #define parameter
            # instantiate
            instanceFactory.Instantiate()
            # end InstanceFactory
            instanceFactory.EndInstantiate()
            instanceFactory.EndInstanceFactory()
            if updatebool == True: part.updateobject(instanceFactory)

    class measure(object):
        @staticmethod
        def measureGetShapeGeometryName(GeometryObject):
            '''通过测量获得几何对象的类别，如圆柱，直线等'''
            doc = mydpfun.getDpApplication().activedocument
            spaworkbench = doc.GetWorkbench("SPAWorkbench")
            measurable = spaworkbench.GetMeasurable(GeometryObject)
            catMeasurableName = (
                "CatMeasurableUnknown",
                "CatMeasurable",
                "CatMeasurableVolume",
                "CatMeasurableSurface",
                "CatMeasurableCylinder",
                "CatMeasurableSphere",
                "CatMeasurableCone",
                "CatMeasurablePlane",
                "CatMeasurableCurve",
                "CatMeasurableCircle",
                "CatMeasurableLine",
                "CatMeasurablePoint",
                "CatMeasurableAxisSystem"
            )
            measureableName = catMeasurableName[measurable.GeometryName]
            return measureableName

        @staticmethod
        def measureGetLength(CurveObject):
            doc = mydpfun.getDpApplication().activedocument
            spaWorkbench = doc.GetWorkbench("SPAWorkbench")
            measurable = spaWorkbench.GetMeasurable(CurveObject)
            return measurable.Length

        @staticmethod
        def getPointCoords(dp,pt):
            code = """
            Function GetPointCoord(ByVal obj As AnyObject)
                Dim spaworkbench As SPAWorkbench
                set spaworkbench = Catia.ActiveDocument.GetWorkbench("SPAWorkbench")
                Dim measurable As Measurable
                set measurable = spaworkbench.GetMeasurable(obj)
                Dim coord(2)
                measurable.GetPoint(coord)
                GetPointCoord=coord
            End Function

            """
            coord=dp.SystemService.evaluate(code,1, "GetPointCoord",[pt])
            return coord

        
        @staticmethod
        def measureGetRadius(circleObject):
            doc = mydpfun.getDpApplication().activedocument
            spaWorkbench = doc.GetWorkbench("SPAWorkbench")
            measurable = spaWorkbench.GetMeasurable(circleObject)
            return measurable.Radius

        @staticmethod
        def measureGetArea(SurfaceObject):
            doc = mydpfun.getDpApplication().activedocument
            spaWorkbench = doc.GetWorkbench("SPAWorkbench")
            measurable = spaWorkbench.GetMeasurable(SurfaceObject)
            return measurable.Area
        @staticmethod
        def measureTwoObjectMinDistance(doc,obj1,obj2):
            spaworkbench1 = doc.GetWorkbench("SPAWorkbench")
            measurable1 = spaworkbench1.GetMeasurable(obj1)
            minimumdistance1 = measurable1.GetMinimumDistance(obj2)
            return minimumdistance1




    class create:
        class createPoint:
            @staticmethod
            def createPointByCoord(part, geo, x, y, z, update=False, Name="pt"):
                hsf = part.hybridshapefactory
                pt = hsf.addnewpointcoord(x, y, z)
                pt.name = Name
                geo.appendhybridshape(pt)
                if update == True: part.updateobject(pt)
                return pt
            @staticmethod
            def PointsOnCurveInsertedByPtNumber(part,curveGeo, resultGeo, ptCount=5,iOrientation=True, updatebool=True):                
                '''
                create points on curve by ptCount, include start and end point
                '''
                hsf=part.hybridshapefactory
                resultGeo=part.HybridBodies.item("result")
                iOrientation=0
                for crv in curveGeo.HybridShapes:
                    tempgeo= resultGeo.HybridBodies.Add()
                    tempgeo.Name=crv.Name
                    for i in range(1,ptCount+1):
                        pt=hsf.AddNewPointOnCurveFromPercent(crv,(i-1)/(ptCount-1),iOrientation)
                        tempgeo.AppendHybridShape(pt)
                    print(crv.name)
                if updatebool:
                    part.Update()
            @staticmethod
            def points_on_curve_inserted_by_point_distance(part,osel, result_geo, curve, distance_between_2pt, pt_orientation=True, isplit=-1):
                hsf=part.HybridShapeFactory    
                osel.clear()
                if len(result_geo.HybridBodies) > 0:
                    axis_geo = result_geo.HybridBodies[0]
                    pt_geo = result_geo.HybridBodies[1]
                    sphere_geo = result_geo.HybridBodies[2]
                    split_geo = result_geo.HybridBodies[3]
                else:
                    axis_geo = result_geo.HybridBodies.add()
                    axis_geo.Name="axisGeo"
                    pt_geo = result_geo.HybridBodies.add()
                    pt_geo.Name="ptGeo"
                    sphere_geo = result_geo.HybridBodies.add()
                    sphere_geo.Name="sphereGeo"
                    split_geo = result_geo.HybridBodies.add()
                    split_geo.Name="splitGeo"

                pt = hsf.AddNewPointOnCurveFromPercent(curve, 0, pt_orientation)
                pt_geo.AppendHybridShape(pt)
                part.UpdateObject(pt)

                isolate_pt = hsf.AddNewPointDatum(pt)
                result_geo.AppendHybridShape(isolate_pt)
                part.UpdateObject(pt)
                isolate_pt.Name=f"point_{len(result_geo.HybridShapes)}"

                part.InWorkObject  = axis_geo
                axis = part.AxisSystems.add()
                part.UpdateObject(axis)

                sphere = hsf.AddNewSphere(isolate_pt, None, distance_between_2pt, -90.0, 90.0, 0.0, 360.0) #axis
                sphere_geo.AppendHybridShape(sphere)
                part.UpdateObject(sphere)
                split = hsf.AddNewHybridSplit(curve, sphere, isplit)
                split_geo.AppendHybridShape(split)
                try:
                    part.UpdateObject(split)
                except Exception:
                    pt_end = hsf.AddNewPointOnCurveFromPercent(curve, 1, pt_orientation)
                    pt_geo.AppendHybridShape(pt_end)
                    part.UpdateObject(pt_end)
                    isolate_pt_end = hsf.AddNewPointDatum(pt_end)
                    result_geo.AppendHybridShape(isolate_pt_end)
                    part.UpdateObject(isolate_pt_end)
                    isolate_pt_end.Name=f"point_{len(result_geo.HybridShapes)}"

                try:
                    temp_length = mydpfun.measure.measureGetLength(split)
                    if temp_length > distance_between_2pt and str(temp_length) != str(distance_between_2pt):
                        mydpfun.create.createPoint.points_on_curve_inserted_by_point_distance(part,osel,result_geo, split, distance_between_2pt, pt_orientation, isplit)
                    else:
                        last_pt1 = hsf.AddNewPointOnCurveFromPercent(split, 0, pt_orientation)
                        pt_geo.AppendHybridShape(last_pt1)
                        part.UpdateObject(last_pt1)
                        isolate_last_pt1 = hsf.AddNewPointDatum(last_pt1)
                        result_geo.AppendHybridShape(isolate_last_pt1)
                        part.UpdateObject(isolate_last_pt1)
                        isolate_last_pt1.Name=f"point_{len(result_geo.HybridShapes)}"

                        last_pt2 = hsf.AddNewPointOnCurveFromPercent(split, 1, pt_orientation)
                        pt_geo.AppendHybridShape(last_pt2)
                        part.UpdateObject(last_pt2)
                        isolate_last_pt2 = hsf.AddNewPointDatum(last_pt2)
                        result_geo.AppendHybridShape(isolate_last_pt2)
                        part.UpdateObject(isolate_last_pt2)
                        isolate_last_pt2.Name=f"point_{len(result_geo.HybridShapes)}"
                except Exception:
                    pass

                try:
                    if len(result_geo.HybridBodies) > 0:
                        osel.add(pt_geo)
                        osel.add(axis_geo)
                        osel.add(sphere_geo)
                        osel.add(split_geo)
                        osel.delete()
                        print("finish")
                except Exception:
                    pass

                
        class createLine:
            @staticmethod
            def createLinePtPt(part, resultGeo, pt1, pt2, updatebool=True) -> object:
                hsf = part.hybridshapefactory
                line = hsf.addnewlineptpt(pt1, pt2)
                resultGeo.appendhybridshape(line)
                if updatebool == True: part.updateobject(line)
                return line

            @staticmethod
            def createLinePtPtExtended(part, resultGeo, pt1, pt2, double1=0, double2=0, updatebool=True):
                hsf = part.hybridshapefactory
                line = hsf.AddNewLinePtPtExtended(pt1, pt2, double1, double2)
                resultGeo.appendhybridshape(line)
                if updatebool == True: part.updateobject(line)
                return line

        @staticmethod
        def create_SweepCircle_Surface(part,hsf,resultGeo,curve,radius=200):
            referenceLine=part.CreateReferenceFromObject(curve)
            sweepCircle=hsf.AddNewSweepCircle(referenceLine)
            sweepCircle.Mode=6
            sweepCircle.SetRadius(1,radius)
            resultGeo.AppendHybridShape(sweepCircle)
            return sweepCircle

        @staticmethod
        def createHybridBody(hybridbodies_Object,hybridbody_Name="tempgeo"):
            geo=hybridbodies_Object.add()
            geo.name=hybridbody_Name
            return geo

        @staticmethod
        def createSphere(part, resultgeo, pt, radius, updatebool=True):
            vbhost = win32com.client.Dispatch("ScriptControl")
            vbhost.language = "vbscript"
            vbhost.addcode("""
                    function createSphere(part,resultgeo,pt,radius,updatebool)                                
                    set hsf=part.hybridshapefactory
                    set sphere=hsf.addnewsphere(pt,nothing,radius,-45,45,0,180)
                    sphere.Limitation = 1
                    resultgeo.appendhybridshape(sphere)
                    if updatebool=True then part.updateobject(sphere)
                    'createSphere= sphere
                    end function""")
            vbhost.Run("createSphere", part, resultgeo, pt, radius, updatebool)
            sphere = resultgeo.hybridshapes.item(resultgeo.hybridshapes.count)
            return sphere

        @staticmethod
        def createIntersection(element1, element2, resultGeo, extendMode=3, updatebool=True):
            """extend mode
             ExtendMode is 0 when both "Extend Linear Supposr for intersection" are unchecked
             ExtendMode is 1 when "Extend Linear Supposr for intersection" for First Element is checked and for Second Element is unchecked
             ExtendMode is 2 when "Extend Linear Supposr for intersection" for First Element is unchecked and for Second Element is checked
             ExtendMode is 3 when both "Extend Linear Supposr for intersection" are checked
            """
            part = mydpfun.partDefinedByObject(resultGeo)
            hsf = part.hybridshapefactory
            intersect = hsf.AddNewIntersection(element1, element2)
            intersect.ExtendMode = extendMode
            resultGeo.appendhybridshape(intersect)
            if updatebool == True: part.updateobject(intersect)
        @staticmethod
        def createFillByBoundaryCurve(part, hsf,resultGeo,boundaryCurve):
            fill = hsf.AddNewFill()
            fill.AddBound(boundaryCurve)
            resultGeo.appendhybridshape(fill)
            part.UpdateObject(fill)
            return fill
        @staticmethod
        def createFillByBoundaryCurveList(part,hsf,resultGeo,boundaryCurveList):
            fillList=[]
            for curve in boundaryCurveList:
                fill=hsf.AddNewFill()
                fill.AddBound(curve)
                resultGeo.AppendHybridShape(fill)
                try:
                    part.UpdateObject(fill)
                except:
                    print("update error: ",fill.name)
                fillList.append(fill)
            return fillList
        @staticmethod
        def createExtrudeByElementList(part,hsf,resultGeo,offset1,offset2,direction,elementList):
            extrudelist=[]
            for element in elementList:
                extrude=hsf.AddNewExtrude(element,offset1,offset2,direction)
                resultGeo.appendhybridshape(extrude)
                try:
                    part.updateobject(extrude)
                except:
                    print("update error: ",extrude.name)
                extrudelist.append(extrude)
            return extrudelist
    class selection:
        @staticmethod
        def selectSingleAnyobject(osel):
            osel.clear()
            type = ["AnyObject"]
            mysel = osel.SelectElement2(type, "select object", False)
            obj = osel.item(1).value
            osel.clear()
            return obj

        @staticmethod
        def selectSingleAnyobjectByObjType(osel, objType="AnyObject"):
            osel.clear()
            type = [objType]
            mysel = osel.SelectElement2(type, "select object", False)
            obj = osel.item(1).value
            osel.clear()
            return obj

        @staticmethod
        def selectSinglePlanarFace(osel, objType="PlanarFace"):
            osel.clear()
            type = [objType]
            mysel = osel.SelectElement2(type, "select object", False)
            obj = osel.item(1).value
            osel.clear()
            return obj

        @staticmethod
        def selectSingleFace(osel, objType="Face"):
            osel.clear()
            type = [objType]
            mysel = osel.SelectElement2(type, "select object", False)
            obj = osel.item(1).value
            osel.clear()
            return obj

        @staticmethod
        def selectSingleCylindricalFace(osel, objType="CylindricalFace"):
            osel.clear()
            type = [objType]
            mysel = osel.SelectElement2(type, "select object", False)
            obj = osel.item(1).value
            osel.clear()
            return obj

        @staticmethod
        def selectSingleEdge(osel, objType="Edge"):
            osel.clear()
            type = [objType]
            mysel = osel.SelectElement2(type, "select object", False)
            obj = osel.item(1).value
            osel.clear()
            return obj

        @staticmethod
        def selectSingleVertex(osel, objType="Vertex"):
            osel.clear()
            type = [objType]
            mysel = osel.SelectElement2(type, "select object", False)
            obj = osel.item(1).value
            osel.clear()
            return obj

        @staticmethod
        def selectionToArray(osel):
            '''
            get current selected to array
            '''
            array = [osel.item(x + 1).value for x in range(0, osel.count)]
            return array
        
        @staticmethod
        def selection_get_first_obj(osel):
            '''
            get current selected to array
            '''
            array = [osel.item(x + 1).value for x in range(0, osel.count)]
            
            return array[0]

        @staticmethod
        def selectMultiAnyobject(osel):
            """enum CATMultiSelectionMode {
              CATMonoSel,
              CATMultiSelTriggWhenSelPerf,
              CATMultiSelTriggWhenUserValidatesSelection
            }
            """
            osel.clear()
            type = ["AnyObject"]
            mysel = osel.SelectElement3(type, "select object", True, 2, False);
            sellist = [osel.item(x + 1).value for x in range(0, osel.count)]
            osel.clear()
            return sellist

        @staticmethod
        def selectMultiAnyobjectByObjType(osel, ObjType="AnyObject"):
            """enum CATMultiSelectionMode {
              CATMonoSel,
              CATMultiSelTriggWhenSelPerf,
              CATMultiSelTriggWhenUserValidatesSelection
            }
            """
            osel.clear()
            type = [ObjType]
            mysel = osel.SelectElement3(type, "select object", True, 2, False);
            sellist = [osel.item(x + 1).value for x in range(0, osel.count)]
            osel.clear()
            return sellist

    class direction:
        @staticmethod
        def getDirectionByPlaneOrLine(hsf,element):
            dir=hsf.AddNewDirection(element)
            return dir
    class search:
        pass

class mycadfun(object):
    @staticmethod
    def getAutocadApp():
        # myapp =  win32com.client.dynamic.Dispatch("Autocad.Application")
        myapp =  comtypes.client.GetActiveObject("Autocad.Application")
        return myapp 

    @staticmethod
    def getActiveDocument(app):
        doc=app.ActiveDocument
        return doc
    @staticmethod
    def getModelSpace(doc):
        myModelSpace=doc.ModelSpace
        return myModelSpace

    @staticmethod
    def createPointByCoords(ms,x,y,z):
        coords=array.array('d',[x,y,z])
        pt=ms.AddPoint(coords)
        return pt
    @staticmethod
    def createLineByPTPT_Coordinates(ms,x1,y1,z1,x2,y2,z2):
        coords1=array.array('d',[x1,y1,z1])
        coords2=array.array('d',[x2,y2,z2])
        line=ms.AddLine(coords1,coords2)
        return line
    
    @staticmethod
    def dimensionPtPt(modelSpace, pt1,pt2, TextPosition,TextHeight=100):
        dimension1= modelSpace.AddDimAligned(pt1,pt2,TextPosition)
        dimension1.TextHeight=TextHeight

    @staticmethod
    def dimension3PointAngular(modelSpace, anglePT,PT1,PT2, TextPosition,TextHeight=100):
        dimension1=modelSpace.AddDim3PointAngular(anglePT,PT1,PT2,TextPosition)
        dimension1.TextHeight=TextHeight
    
if __name__ == "__main__":
    dp = mydpfun.getDpApplication()
    doc=dp.ActiveDocument
    osel=doc.Selection
    part=doc.Part
    hsf=part.HybridShapeFactory
    parameters=part.Parameters
    for p in parameters:
        print(p.Name)
    print(doc.name)

    
    
    
    print("test")

