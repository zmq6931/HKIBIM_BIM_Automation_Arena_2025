# __author__ = 'Andy'
# -*- coding: utf-8 -*-

import rhinoscript
from rhinoscript.curve import CurveClosestPoint
from rhinoscript.object import ObjectMaterialIndex
import rhinoscriptsyntax as rs
import Rhino as rh
import sys as sys
import System
import time , os,shutil
import scriptcontext as sc
import math


class folder_files(object):
    @staticmethod
    def get_all_file_path_include_Subfolder(folderFullPath):
        result = []
        for maindir, subdir, file_name_list in os.walk(folderFullPath):
            for filename in file_name_list:
                apath = os.path.join(maindir, filename)
                result.append(apath)
        return result
    @staticmethod
    def get_file_list_under_folder(folderPath):
        subFilePathList=[os.path.join(folderPath,x) for x in os.listdir(folderPath)]
        filePathlist=[x  for x in subFilePathList if os.path.isfile(x)==True]
        return filePathlist

#---------------------------------------------------------------------------------------------------------
class myfun(object):
    class select:
        @staticmethod
        def selectAllCurves():
            curves=rs.ObjectsByType(4, True, 1)
            return curves
        @staticmethod
        def selectAllMeshes():
            meshes=rs.ObjectsByType(32, True, 1)
            return meshes        
        @staticmethod
        def selectAllPoints():
            pts=rs.ObjectsByType(1,True,1)
            return pts
        
        @staticmethod
        def selectAllSurfaces():
            surfaces=rs.ObjectsByType(8,True,1)
            return surfaces        
        @staticmethod
        def selectAllPolySurfaces():
            PolySurfaces=rs.ObjectsByType(16,True,1)
            return PolySurfaces  
        
        @staticmethod
        def selectSingleAnyObject(typeNumber=0,preselectBool=False):
            obj=rs.GetObject("get any single object by typeNumber",typeNumber,preselectBool)
            return obj
        @staticmethod
        def selectAllObjects(selectBool=True):
            objlist=rs.AllObjects(selectBool)
            return objlist
        @staticmethod
        def toSelectObjects(objectArray):
            rs.SelectObjects(object)
        @staticmethod
        def selectObjectsByLayerIncludeSubLayers(layer,selectBool=True):
            layernames=rs.LayerNames()
            for i in layernames:
                if layer in i:
                    rs.ObjectsByLayer(i,True)
            return rs.SelectedObjects()
        @staticmethod
        def selectedObjects():
            objs=rs.SelectedObjects()
            return objs
        @staticmethod
        def unselectAllObjects():
            rs.UnselectAllObjects()
    class layer:
        @staticmethod
        def selectObjectsByLayer(layer,selectBool=True):
            return rs.ObjectsByLayer(layer,selectBool)
        @staticmethod
        def getObjectLayer(obj):
            return rs.ObjectLayer(obj)
        @staticmethod
        def set_currentLayer(layer):
            return rs.CurrentLayer(layer)
        @staticmethod
        def get_currentLayer():
            return rs.CurrentLayer()   
        @staticmethod
        def selectObjectsByLayerIncludeSubLayers(layer,selectBool=True):
            layernames=rs.LayerNames()
            for i in layernames:
                if layer in i:
                    rs.ObjectsByLayer(i,True)
            return rs.SelectedObjects()
        @staticmethod 
        def getLayerByName(layerName):
            layers=rs.LayerNames()
            for i in layers:
                if i==layerName:
                    return i
            return None
    class line:
        @staticmethod
        def createLinePtPt(pt1,pt2):
            return rs.AddLine(pt1,pt2)
        @staticmethod
        def create_Normal_Line(plane,pt,length=1000):
            normal=myfun.plane.get_plane_normal(plane)
            scaled_normal = rs.VectorScale(normal, length)
            normal_line = rs.AddLine(pt, rs.PointAdd(pt, scaled_normal))
            return normal_line
                            
    class point:
        @staticmethod
        def createPointByCoord(x,y,z):
            return rs.AddPoint(x,y,z)
        @staticmethod
        def createPointByCoordArray(xyzArray):
            return rs.AddPoint(xyzArray)
        @staticmethod
        def coordinatesToMathPoint(pointArray):
            return rs.PointAdd([0,0,0],pointArray)
        @staticmethod
        def getPointCoords(pt):
            return rs.PointCoordinates(pt)
        @staticmethod
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
        @staticmethod
        def sameDistancePointOnCurve(curve,distance,reserveBool=False):
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
        @staticmethod
        def sameDistancePointIdOnCurve(curve,distance,reserveBool=False):
            if reserveBool:
                rs.ReverseCurve(curve)
            temp=[]
            ptlist=rs.DivideCurveEquidistant(curve,distance,False)
            for pt in ptlist:
                temppt=rs.AddPoint(pt)
                temp.append(temppt)  
            endpt=rs.CurveEndPoint(curve)
            distance= rs.Distance(ptlist[len(ptlist)-1],endpt)  
            if round(distance,5)!=0 :
                temppt=rs.AddPoint(endpt)
                temp.append(temppt)
            return temp       
    class circle:
        @staticmethod
        def createCircleByPt(centerPt,radius):
            return rs.AddCircle(centerPt,radius)        
    class sphere:
        @staticmethod
        def createSphereByPtAndRadius(pt,radius):
            return rs.AddSphere(pt,radius)
    class move:
        @staticmethod 
        def moveObject(obj,translationXYZ):
            rs.MoveObject(obj,translationXYZ)     
    class my_time:
        @staticmethod
        def sleep(doubleSecond):
            """import second"""
            time.sleep(doubleSecond)
    class show:
        @staticmethod
        def hideObjects(objlist):
            rs.HideObjects(objlist)
        @staticmethod
        def showObjects(objlist):
            rs.ShowObjects(objlist)
    class object:
        @staticmethod
        def get_Selected_Objects():
            selected_objs=rs.SelectedObjects()
            return selected_objs
        @staticmethod
        def getObjectName(obj):
            '''this object from other software'''
            name=rs.ObjectName(obj)            
            return name
        @staticmethod
        def changeObjectColor(objids,color=(255,0,0)):
            rs.ObjectColor(objids,color)
        @staticmethod
        def getObjectMaterialColor(objid):
            color=rs.MaterialColor(rs.ObjectMaterialIndex(objid))
            return color
    class string:
        @staticmethod
        def replace_special_string(str):
            newstr = str.replace('?', '_').replace('*', '_'). \
            replace(':', '_').replace(';', '_').replace('"', '_'). \
            replace("'", '_').replace('<', '_').replace('>', '_'). \
            replace('\\', '_').replace('/', '_').replace('|', '_'). \
            replace('.', '_').replace(',', '_')
            return newstr
    class curve:
        @staticmethod
        def reverseCurve(curve):
            """return bool, mean success or failure"""
            return rs.ReverseCurve(curve)
    class measure:
        @staticmethod
        def curveLength(curve):
            return rs.CurveLength(curve)
        @staticmethod
        def surfaceArea(surface):
            surfArea=rs.SurfaceArea(surface)
            area=surfArea[0] + surfArea[1]
            return area
    class text:
        @staticmethod
        def createText(textString,positionPoint,height=1.0,font="Arial",font_style=0):
            return rs.AddText(textString,positionPoint,height,font="Arial",font_style=0)
    class get:
        @staticmethod
        def get_object_name(objid):
            return rs.ObjectName(objid)
        @staticmethod
        def get_Selected_Objects():
            selected_objs=rs.SelectedObjects()
            return selected_objs
        @staticmethod
        def getReal():
            return rs.GetReal()
        @staticmethod
        def get_mesh_center_point_coordinates(objid):
            centerpt=rs.MeshAreaCentroid(objid)
            return centerpt[0]
        @staticmethod
        def get_all_objects_under_layer(layerName):
            layer_objects = rs.ObjectsByLayer(layerName)
            return layer_objects
        @staticmethod
        def get_curves_under_layer(layerName):
            layer_objects = rs.ObjectsByLayer(layerName)
            curves=[obj for obj in layer_objects if rs.IsCurve(obj)]

            return curves
        @staticmethod
        def get_surfaces_under_layer(layerName):
            layer_objects = rs.ObjectsByLayer(layerName)
            surfaces=[obj for obj in layer_objects if rs.IsSurface(obj)]
            return surfaces
    class plane:
        @staticmethod
        def create_surface_normal_plane_by_pt(surface,pt, bool_if_create_plane_surface=False):
            param = rs.SurfaceClosestPoint(surface, pt)
            normal=rs.SurfaceNormal(surface,param)
            plane=rs.PlaneFromNormal(pt,normal)
            if bool_if_create_plane_surface:
                rs.AddPlaneSurface(plane,500,500)
            return plane
        @staticmethod
        def set_current_cplane(plane):
            rs.ViewCPlane(None, plane)
        @staticmethod
        def get_plane_normal(plane):
            return plane.ZAxis
    class hexagon:
        @staticmethod
        def create_hexagonal_edge_6(pt1,pt2):
            center = [(pt1[0] + pt2[0])/2, (pt1[1] + pt2[1])/2, (pt1[2] + pt2[2])/2]
            pt2=rs.RotateObject(pt1,center,60,axis=None,copy=True)
            pt3=rs.RotateObject(pt1,center,120,axis=None,copy=True)
            PT4=rs.RotateObject(pt1,center,180,axis=None,copy=True)
            PT5=rs.RotateObject(pt1,center,240,axis=None,copy=True)
            PT6=rs.RotateObject(pt1,center,300,axis=None,copy=True)
            tempHexago=rs.AddPolyline([pt1,pt2,pt3,PT4,PT5,PT6,pt1])
            rs.DeleteObjects([pt2,pt3,PT4,PT5,PT6])
            return tempHexago
        @staticmethod
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

        @staticmethod
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
        @staticmethod
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
        



        
    class useful_Fun:
        @staticmethod
        def export_objects_by_layer(folderPath,layerName,formatString=".igs"):
            layer=layerName        #import layer name
            format=formatString        #import format
            #export folder path
            exportFolderPath=folderPath
            for item in rs.LayerChildren(layer):
            #    objects=selectObjectsByLayer(item)
                objects=myfun.select.selectObjectsByLayerIncludeSubLayers(item)
            #    name =replace_special_string( item.split("::")[len(item.split("::"))-1]) #replace_special_string(item) #仅当前图层名
                name =myfun.string.replace_special_string(item) #图层全路径
                fileFullPath = " "+"\""+exportFolderPath + "\\"+ name + format+"\""
                command1 = "-_Export" + fileFullPath + " Enter"   #  + " Enter"
                rs.Command(command1,True)
                rs.UnselectObjects(objects)
                print(name)
            print("finish")
        @staticmethod
        def extract_Mesh_Edge_By_SelectedObjects(objs):
            for mesh in objs:
                rs.UnselectAllObjects()
                rs.SelectObject(mesh)
                command1 = "-ExtractMeshEdges" + " Enter"   #  + " Enter"
                rs.Command(command1,True)
                rs.UnselectAllObjects()
        @staticmethod
        def import_FBX_then_export_to_DWG(fbx_folder,dwg_folder):
            # fbx_folder=r"C:\Users\Administrator\Desktop\dddwg\New folder (11)\ABFA - Copy"
            # dwg_folder=r"C:\Users\Administrator\Desktop\dddwg\New folder (11)\ABFA - Copy\New folder"
            filePathList=folder_files.get_file_list_under_folder(fbx_folder)
            for file in filePathList:
                print(os.path.split(file)[1])
                dwgFilePath=os.path.join(dwg_folder,os.path.split(file)[1].replace(".fbx",".dwg"))
                rs.DocumentModified(False)
                rs.Command("_-New _None",True)
                command1="_-Open " + "\"" + file + "\"" + " Enter"
                rs.Command(command1,True)
                commandExport="_-Export " + "\"" + dwgFilePath+"\"" +" Enter"
                select_objs=rs.ObjectsByType(4, True, 1)
                rs.DeleteObjects(select_objs)
                myfun.select.selectAllObjects()
                rs.Command(commandExport,True)
                # myfun.select.unselectAllObjects()
            print("finish")
        @staticmethod
        def import_FBX_then_export_to_DWG_With_Material_Color(fbx_folder,dwg_folder):
            # fbx_folder=r"C:\Users\Administrator\Desktop\dddwg\New folder (11)\ABFA - Copy"
            # dwg_folder=r"C:\Users\Administrator\Desktop\dddwg\New folder (11)\ABFA - Copy\New folder"
            filePathList=folder_files.get_file_list_under_folder(fbx_folder)
            for file in filePathList:
                print(os.path.split(file)[1])
                dwgFilePath=os.path.join(dwg_folder,os.path.split(file)[1].replace(".fbx",".dwg"))
                rs.DocumentModified(False)
                rs.Command("_-New _None",True)
                command1="_-Open " + "\"" + file + "\"" + " Enter"
                rs.Command(command1,True)
                commandExport="_-Export " + "\"" + dwgFilePath+"\"" +" Enter"
                select_objs=rs.ObjectsByType(4, True, 1)
                rs.DeleteObjects(select_objs)
                select_objs=rs.ObjectsByType(1, True, 1)
                rs.DeleteObjects(select_objs)
                objectlist= myfun.select.selectAllObjects()
                for objid in objectlist:
                    try:
                        materialcolor=myfun.object.getObjectMaterialColor(objid)
                        myfun.object.changeObjectColor(objid,materialcolor)
                    except:
                        pass
                rs.Command(commandExport,True)
                # myfun.select.unselectAllObjects()
            print("finish")
        @staticmethod
        def input_file_Extract_Mesh_Edge_and_export_edge_curve_to_igs(input_folder,output_folder):                      
            filePathList=folder_files.get_file_list_under_folder(input_folder)
            for file in filePathList:
                rs.DocumentModified(False)  
                outputFilePath=os.path.join(output_folder,os.path.split(file)[1].split(".")[0]+".igs")
                # rs.Command("_-New _None",True)
                command1="_-Open " + "\"" + file + "\"" + " Enter"
                rs.Command(command1,True)
                commandExport="_-Export " + "\"" + outputFilePath+"\"" +" Enter"
                select_objs=rs.ObjectsByType(32, True, 1)
                myfun.useful_Fun.extract_Mesh_Edge_By_SelectedObjects(select_objs)
                myfun.select.unselectAllObjects()        
                select_objs=myfun.select.selectAllCurves()
                rs.Command(commandExport,True)
        @staticmethod
        def import_FBX_then_export_to_wrl(fbx_folder,wrl_folder):
            # fbx_folder=r"C:\Users\Administrator\Desktop\dddwg\New folder (11)\ABFA - Copy"
            # dwg_folder=r"C:\Users\Administrator\Desktop\dddwg\New folder (11)\ABFA - Copy\New folder"
            filePathList=folder_files.get_file_list_under_folder(fbx_folder)
            for file in filePathList:
                print(os.path.split(file)[1])
                wrlFilePath=os.path.join(wrl_folder,os.path.split(file)[1].replace(".fbx",".wrl"))
                rs.DocumentModified(False)
                rs.Command("_-New _None",True)
                command1="_-Open " + "\"" + file + "\"" + " Enter"
                rs.Command(command1,True)
                commandExport="_-Export " + "\"" + wrlFilePath+"\"" +" Enter"
                select_objs=rs.ObjectsByType(4, True, 1)
                rs.DeleteObjects(select_objs)
                myfun.select.selectAllObjects()
                rs.Command(commandExport,True)
                # myfun.select.unselectAllObjects()
            print("finish")
    class export:
        @staticmethod
        def export_objects_by_layer(folderPath,layerName,formatString=".igs"):
            layer=layerName        #import layer name
            format=formatString        #import format
            #export folder path
            exportFolderPath=folderPath
            for item in rs.LayerChildren(layer):
            #    objects=selectObjectsByLayer(item)
                objects=myfun.select.selectObjectsByLayerIncludeSubLayers(item)
            #    name =replace_special_string( item.split("::")[len(item.split("::"))-1]) #replace_special_string(item) #仅当前图层名
                name =myfun.string.replace_special_string(item) #图层全路径
                fileFullPath = " "+"\""+exportFolderPath + "\\"+ name + format+"\""
                command1 = "-_Export" + fileFullPath + " Enter"   #  + " Enter"
                rs.Command(command1,True)
                rs.UnselectObjects(objects)
                print(name)
            print("finish")

        @staticmethod
        def export_to_iges(fullpath):
            rs.UnselectAllObjects()
            rs.SelectObjects(rs.AllObjects())    
            fileFullPath = " \""+fullpath+"\""
            command = "-_Export "+fileFullPath+" Enter"
            rs.Command(command, True)



def select_visible():
    rs.CurrentView("Prespective")
    rs.Command("_SelVisible")
    


if __name__=="__main__":

    # path=r"C:\Users\Administrator\Desktop\dddwg\New folder (15)"
    # myfun.export.export_objects_by_layer(path,"Layer 01",".igs")

    select_visible()

    
    print("tttfinish")


