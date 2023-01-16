#!/usr/bin/env python3
#MIT License

#Copyright (c) 2022 hramacha

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


import os
import json
from utils import progressbar
from pathlib import Path

DebugLevel = 0

class DeviceInfoClass:
    def __init__(self, interfacetype, deviceid):
        self.InterfaceType = interfacetype
        self.DeviceID = deviceid

class DeviceScannerElementClass: 
    def __init__(self):
        self.FileName = None
        self.DeviceType = ""
        self.Description = ""
        self.DeviceInfoList = []
        self.CompatibleList = []
        self.DriverInformation = ""
        self.DeviceTreeInformation = ""

class DeviceCatalogClass:
    def __init__(self, cFile):
        self.CatalogFile = cFile
        self.LinuxVersion = None
        self.DeviceCatalog = None
        self.DeviceDataList = []

    def UpdateDeviceCatalog(self):
        dCatalogFile = open(self.CatalogFile, "r")
        data = json.load(dCatalogFile)
        self.LinuxVersion = data["LinuxVersion"]
        DevCatalog = data["DeviceCatalogDatabase"]
        if DevCatalog != None: 
            for i in progressbar(range(len(DevCatalog)), "Reading Device Catalog : ", 100):
                DevEntry = DevCatalog[i]
                if type(DevEntry) is dict:
                    DeviceScannerElement = DeviceScannerElementClass()
                    DeviceScannerElement.FileName = DevEntry.get("FileName");
                    DeviceScannerElement.DeviceType = DevEntry.get("DeviceType");
                    DeviceScannerElement.Description = DevEntry.get("Description");
                    DeviceScannerElement.DriverInformation = DevEntry.get("DriverInformation");
                    if len(DevEntry.get("Devices")) != 0 :
                        for j in range(0, len(DevEntry.get("Devices"))):
                            DeviceEntry = DevEntry.get("Devices")[j]
                            DeviceInfo = DeviceInfoClass(DeviceEntry.get("InterfaceType"), DeviceEntry.get("DeviceID"))
                            DeviceScannerElement.DeviceInfoList.append(DeviceInfo)
                    if len(DevEntry.get("Compatible")) != 0 :
                        for j in range(0, len(DevEntry.get("Compatible"))):
                            CompatibleEntry = DevEntry.get("Compatible")[j]
                            CompatibleInfo = DeviceCompatibleJsonDataClass(CompatibleEntry.get("Manufacturer"), CompatibleEntry.get("DeviceName"))
                            DeviceScannerElement.CompatibleList.append(CompatibleInfo)
                    #print(DeviceScannerElement.FileName, "\t", DeviceScannerElement.DeviceType)
                    self.DeviceDataList.append(DeviceScannerElement)
        self.DeviceCatalog = DevCatalog

    def SearchForDeviceType(self,device):
        if device == ';':
            return None

        #print(len(self.DeviceDataList))        
        for i in range(0, len(self.DeviceDataList)):
            ddl = self.DeviceDataList[i]            
            if len(ddl.DeviceInfoList) > 0: 
                for dil in ddl.DeviceInfoList:
                    if len(dil.DeviceID) == 0:
                        continue
                    #if len(dil.DeviceID) > len(device):
                    #    if device in dil.DeviceID:
                    #        return ddl
                    #elif len(dil.DeviceID) < len(device):
                    #    if dil.DeviceID in device:
                    #        return ddl
                    #else:
                    if dil.DeviceID == device:
                        return ddl
            if len(ddl.CompatibleList) > 0: 
                for cil in ddl.CompatibleList:
                    if len(cil.DeviceName) == 0:
                        continue
                    #if len(cil.DeviceName) > len(device):
                    #    if device in cil.DeviceName:
                    #        return ddl
                    #elif len(cil.DeviceName) < len(device):
                    #    if cil.DeviceName in device:
                    #        return ddl
                    #else:
                    if cil.DeviceName == device:
                        return ddl        
        return None

class PairClass:
    def __init__(self, K, V):
        self.Key = K
        self.Value = V
        self.VValues = []
    
    def getKey(self):
        return self.Key
    
    def getValue(self):
        return self.Value

class DeviceListInfoClass:
    def __init__(self, deviceInfo, DataRecord):
        self.DeviceInfo = deviceInfo
        self.DataRecord = DataRecord
        self.Count = 1

class DeviceCompatibleJsonDataClass:
    def __init__(self, manufacturer, deviceName):
        self.Manufacturer = str(manufacturer)
        self.DeviceName = str(deviceName)
        self.DTReference = ""

    def getManufacturer(self):
        return self.Manufacturer

    def getDeviceName(self):
        return self.DeviceName

    def setManufacturer(self, Manufacturer):
        self.Manufacturer = Manufacturer

    def setDeviceName(self, DeviceName):
        self.DeviceName = DeviceName    

class DataPairClass:
    def __init__(self, k, v):
        self.key = k
        self.value = v
    
    def getKey(self):
        return self.key
    
    def getValue(self):
        return self.value

class DataElementInfoClass:
    def __init__(self):
        self.ElementType = None
        self.ElementString = None
        self.AliasReference = None
        self.MultiLineString = []
        self.DataTokenList = []

class DataTokenClass: 
    def __init__(self):
        self.Header = None
        self.Tokens = []

class DTSAliasClass: 
    def __init__(self):
        self.AliasName = None
        self.AliasDataInfo = None

class DTSCompatibleClass:
    def __init__(self):
        self.CompatibleString = None
        self.CompatibleList = []
        
    def AddCompatibleData(self, Data):
        # Remove some of the unncessary charecters                 
        
        CString = Data.split("\"")
        CList = []
        for i in range(0, len(CString)):
            s = CString[i].replace(" ", "").replace("", "")
            if len(s) == 0 :
                continue
            if s == ",":
                continue
            CList.append(s)

        Manufacturer = None
        for s in  CList:
          if "," in s:
            
            self.CompatibleList.append(tuple((s.split(",")[0], s.split(",")[1])))
            Manufacturer = s.split(",")[0]
          else:
              self.CompatibleList.append(tuple((Manufacturer, s)))

class DTSContentClass:
    def __init__(self):
        self.ContentList = []
        self.DTSContentList = []

class EepromDTSDataClass:
    def __init__(self):
        self.DataInfo = None
        self.Name = None
        self.I2CDevice = None

class LEDClass:
    def __init__(self):
        self.Source = None
        self.Status = None
        self.LineInfo = None

class GPIOI2CExtTypeClass:
    def __init__(self):
        self.Type = None
        self.Reg = None    

class GPIOI2CExtClass:
    def __init__(self):
        self.I2CGPIOExtInfo = None
        self.ExtType = None
        self.GPIOLine = None

class GPIOLineClass:
    def __init__(self):
        self.LineID = None
        self.LineName = None
        self.defaultState = None
        self.GPIOString = None
        self.LineSource = None

class GPIOKeysClass:
    def __init__(self):
        self.Label = None
        self.LineInfo = None
        self.LinuxCode = None

class GPIOKeysPolledClass:
    def __init__(self):
        self.PollInterval = 0
        self.GPIOKeys = None

class GPIODTSDataClass:
    def __init__(self):            
        self.DataInfo = None
        self.Status = None
        self.Source = None
        self.InterfaceType = None
        self.ControllerType = None
        self.GPIOI2CExt = None
        self.CompatibleList = []
        self.LED = None
        self.GPIOLine = None
        self.GPIOKeys = None
        self.GPIOKeysPolled = None
     
    def CreateLED(self):
        self.Source = str("LED")        
        self.LED = LEDClass()
        self.LED.LineInfo = GPIOLineClass()
        
    def CreateGPIOLine(self):
        self.Source = str("GPIOLine")
        self.GPIOLine = GPIOLineClass()        
        
    def CreateGPIOI2CExt(self, t):
        self.Source = "GPIOExt"      
        GPIOI2CExt = GPIOI2CExtClass()
        if t == "ExtType":
            self.GPIOI2CExt.ExtType = GPIOI2CExtTypeClass()
        else:
            self.GPIOI2CExt.GPIOLine = GPIOLineClass()
    
    def CreateGPIOKeys(self):
        self.Source = "GPIOKeys"
        self.GPIOKeys = GPIOKeysClass()        
        self.GPIOKeys.LineInfo = GPIOLineClass()
    
    def CreateGPIOKeysPolled(self):
        self.Source = "GPIOKeysPolled"
        self.GPIOKeysPolled = GPIOKeysPolledClass()  
        self.GPIOKeysPolled.GPIOKeys = GPIOKeysClass()        
        self.GPIOKeysPolled.GPIOKeys.LineInfo = GPIOLineClass()  

class I2CBusDataClass:
    def __init__(self): 
        self.DataInfo = None
        self.BusId = None
        self.PhysicalBusLocation = None
        self.LogicalBusLocation = None
        self.Parent = None
        self.Alias = None
        self.BusLevel = None
        self.BusType = None
        self.BusFrequency = None
        self.BusName = None
        self.Status = None
        self.DebugState = None
        self.LockState = None
        self.LockPolicy = None
        self.Reg = None
        self.AddressCells = None
        self.SizeCells = None
        self.BusProtocol = None
        self.VoltageRail = None        
        self.DeviceList = []

class I2CDeviceDataClass:
    def __init__(self): 
        self.DataInfo = None
        self.PhysicalBusLocation = None
        self.LogicalBusLocation = None
        self.I2CId = None        
        self.PlatformID = None  
        self.DTSName = None
        self.DriverClass = None
        self.DeviceType = None
        self.SlaveAddress = None
        self.DTSLabel = None
        self.AliasName = None        
        self.CompatibleList = []
        self.Reg = None
        self.AddressCells = None
        self.SizeCells = None
        self.Status = None
        self.DebugState = None
        self.I2CSubDeviceList = []
        self.ParentBus = None
        self.ParentDevice = None
        self.I2CSecBusList = []
        self.GPIOList = []

class IioHwmonDTSDataClass:
    def __init__(self):    
        self.Status = None
        self.CompatibleList = []
        self.Name = None
        self.Channel = None
        self.ADCSource = None
        self.DataInfo = None
    
class LEDDTSDataClass:
    def __init__(self):    
        self.DataInfo = None
        self.Source = None   
        self.Status = None
        self.CompatibleList = []
        self.GPIOData = None

class PwmDTSDataClass:
    def __init__(self):    
        self.DeviceInfo = None
        self.InterfaceSource = None
        self.PWMName = None
        self.PwmID = None
        self.PwmDataInfo = None
        self.PwmPinDataInfo = None
        self.TachList = []
    
class PwmTachoDTSDataClass:
    def __init__(self):    
        self.Status = None
        self.PwmPinDataInfo = None
        self.FanDataInfo = None
        self.PwmID = None
        self.FanDeviceInfo = None
        self.FanList = []
    
class TachDTSDataClass:
    def __init__(self):    
        self.TachName = None
        self.TachID = None
        self.FanDeviceInfo = None

class DataInfoClass:
    def __init__(self, dataParent):
        self.DTSDataParent = dataParent
        self.Model = None
        self.CompatibleList = []
        self.BusLevel = None
        self.FuncType = None
        self.FuncAddress = None
        self.FuncAlias = None
        self.AliasRefList = []
        self.DTSAliasReferenceList = []
        self.ElementMap = []  
        self.Parent = None
        self.DataInfoList = []
        self.ParamList = []
        self.TraceMap = None
        
    def ProcessDataHeader(self, ln):

        line = ln

        if "&gpio" in line:
            line = ln


        if '/*' in line and '*/' in line:
            commentstring = ln[ln.index('/*')+2:ln.index('*/')]
            line = ln.replace('/*'+commentstring+'*/', "").strip()
        else:
            line = ln

        line = line.replace("{", "").replace(" ", "")
        if ":" in line and "@" in line:
            self.FuncAlias = line.split(":")[0]
            self.FuncType = line.split(":")[1].split("@")[0]
            #self.FuncAddress = line.split(":")[1].split("@")[1]
            self.FuncAddress = line.split("@")[1]
        elif ":" in line:
            self.FuncAlias = line.split(":")[0]
            self.FuncType = line.split(":")[1]            
        elif "@" in  line:
            self.FuncType = line.split("@")[0]
            self.FuncAddress = line.split("@")[1]                       
        else:
            self.FuncType = line.split("@")[0]
        
        if "&" in line:            
            self.AliasRefList.append(line.replace("&", ""))
    
    def Print(self, print_level, DTSDataParent):        
        if print_level > 4: 
            if DebugLevel == 1: 
                print("ERROR: Scanning the File ... too complex ...sorry")
                self.DTSDataParent.ErrorState = True
            return 
        prefix = ""
        if print_level != 0:
            for i in range(0, print_level): 
                prefix = prefix + "   "

        header = ""
        if self.FuncType != None:
            header = header+ self.FuncType
        
        if self.FuncAddress != None:
            header = header + "@"+ self.FuncAddress

        if self.FuncAlias != None:
            header = header + "("+ self.FuncAlias+")"                           
        
        self.DTSDataParent.BuilderOutput.append("\n\n"+prefix+header)

        prefix = prefix + "\t"
        
        if len(self.DTSAliasReferenceList) > 0:
            for dac in  self.DTSAliasReferenceList:
                if dac.AliasName != self.FuncAlias:
                    dac.AliasDataInfo.Print(print_level+1, DTSDataParent)

        if len(self.ElementMap) != 0 :
            for p  in self.ElementMap:
                if p.ElementString != None:
                    DTSDataParent.BuilderOutput.append("\n"+prefix+ p.ElementString.getKey()+ ":"+str(p.ElementString.getValue()))
                if  len(p.DataTokenList) > 0:
                    if len(p.DataTokenList) == 1:
                        for sss in p.DataTokenList[0].Tokens:
                            DTSDataParent.BuilderOutput.append("\n"+prefix+"\t : "+sss+" ")
                    else:
                        for dtoken in p.DataTokenList:
                            DTSDataParent.BuilderOutput.append("\n"+ prefix+ "\t : "+ dtoken.Header+ " ")
                            for sss in dtoken.Tokens:
                                DTSDataParent.BuilderOutput.append("\n"+ prefix+ "\t\t : "+ sss+ " ")
                elif len(p.MultiLineString) > 0:
                    for s in p.MultiLineString:
                        DTSDataParent.BuilderOutput.append("\n"+ prefix+ "\t "+ s+ " ")

                if p.AliasReference != None:
                    if p.AliasReference.AliasName != self.FuncAlias:
                        p.AliasReference.AliasDataInfo.Print(print_level+1, DTSDataParent)

        if len(self.ParamList) != 0:
            for p in self.ParamList:
                DTSDataParent.BuilderOutput.append("\n"+ prefix+ p+ " : True")

    def ProcessMultiLine(self, MultiLine):
        element = DataElementInfoClass()
        if "=" in MultiLine[0]:
            ss = MultiLine[0].split("=")
            if len(ss) == 1:
                element.ElementString = DataPairClass(ss[0].replace(" ", ""), None)                                
            elif len(ss) > 1:
                element.ElementString = DataPairClass(ss[0].replace(" ", ""), None)  
                if len(ss[1]) != 0: 
                    element.MultiLineString.append(ss[1].replace("<", "").replace(">", ""))
        else:
            return
        
        for i in range(1, len(MultiLine)):
            if "dummy always" in MultiLine[i]:
                element = element

            element.MultiLineString.append(MultiLine[i])

        headerflag = False
        DataToken = None
        token = []
        
        if "/*" in element.MultiLineString[0] and "*/" in element.MultiLineString[0]: 
            headerflag = True
        
        if headerflag == True or "," in element.MultiLineString[0]:
            for s in element.MultiLineString:
                if "dummy always" in s:
                    token = None                    

                if headerflag == True:
                    count_comments = 0
                    index = 0
                    
                    loop_flag = False
                    while loop_flag == False:
                        try:
                            index = s.index("/*", index)                     
                            if index >= 0:
                                if count_comments == 1:
                                    end_index = s.index("*/", index)
                                    commentstring = s[index:end_index+2]
                                    s = s.replace(commentstring, "")
                                    break
                                count_comments += 1
                                index += 1
                        except ValueError:
                            loop_flag = True

                    if "/*" in s and "*/" in s:
                        if DataToken != None:
                            element.ElementType = "gpio-lines"
                            element.DataTokenList.append(DataToken)
                            DataToken = None

                        s = s.replace("/*", "").replace("*/", ",")
                        token = s.split(",")
                        if token == None:
                            DataToken = None

                        DataToken = DataTokenClass()                        
                        DataToken.Header = token[0].replace(" ", "")
                        for i in range(1, len(token)):
                            DataToken.Tokens.append(token[i].replace(" ", "").replace("\"", ""))

                    else:
                        if DataToken != None:
                            token = s.split(",")
                            for i in range(1, len(token)):
                                DataToken.Tokens.append(token[i].replace(" ", "").replace("\"", ""))
                else:
                    if DataToken == None:
                        DataToken = DataTokenClass()
                        element.DataTokenList.append(DataToken)

                    token = s.split(",")                    
                    for i in range(0, len(token)):
                        DataToken.Tokens.append(token[i])        
        
        self.ElementMap.append(element)                        
    
    def ProcessDataInfo(self, line, AliasFlag):
        if line == None:
            return

        if len(line) == 0: 
            return

        if "=" not in line:
            if "" not in line:
                return
            
            if "&" in line or "<" in line or ">" in line:
                return
                
            ss = line.split(";")
            if len(ss) == 1:                
                self.ParamList.append(ss[0])                
                        
            return
                 
        line = line.replace("", "").replace(" =", "=").replace("= ", "=")
        
        ss = line.split("=")
        if len(ss) > 1:
            element = DataElementInfoClass()
            element.ElementType = "Parameters"
            element.ElementString = DataPairClass(ss[0], ss[1].replace("<", "").replace(">", "").replace(", ", ",").replace(" ,", ","))                
            self.ElementMap.append(element)            
        else:
            return
        
        if "model" in line:
             Model = line.split("=")[1]

        if "compatible" in line:
            Compatible = DTSCompatibleClass()
            Compatible.AddCompatibleData(line.replace(";","").split("=")[1])
            self.CompatibleList.append(Compatible)
    
    def ConnectAliases(self):
        if len(self.AliasRefList) > 0:
            for s in  self.AliasRefList:
                for dac in self.DTSDataParent.PlatformDTSData.AliasReference:
                    if dac.AliasName == s:
                        self.DTSAliasReferenceList.append(dac)        

        if self.Parent != None:
            if len(self.Parent.DTSAliasReferenceList) > 0:
                for dac in self.Parent.DTSAliasReferenceList:
                    self.DTSAliasReferenceList.append(dac)
        
        for dei in self.ElementMap:
            if dei.ElementString == None:
                continue

            if dei.ElementString.getValue() == None:
                if len(dei.DataTokenList) == 0:
                    if len(dei.MultiLineString) > 0:
                        for es in  dei.MultiLineString:
                            if "&" in es:
                                s = es.replace("<", "").replace(">", "")
                                ee = s.split(" ")
                                if "&" in ee[0]:
                                    aelement = ee[0].replace("&", "")
                                    for dac in  self.DTSDataParent.PlatformDTSData.AliasReference:
                                        if dac.AliasName == aelement:
                                            dei.AliasReference = dac                                                        
            else:
                if "&" in dei.ElementString.getValue():
                    s = dei.ElementString.getValue().replace("<", "").replace(">", "")
                    ee = s.split(" ")
                    if "&" in ee[0]:
                        aelement = ee[0].replace("&", "")                        
                        for dac in self.DTSDataParent.PlatformDTSData.AliasReference:
                            if dac.AliasName  == aelement:
                                dei.AliasReference = dac
DeviceReference = None 

class PlatformDTSClass:
    def __init__(self):
        self.DTSFileLines = []
        self.PlatformDTSIDataList = []
        self.PlatformDTSFileData = PlatformDTSFileDataClass(self)
        self.DTSFileList = []
        self.DTSContentList = [] 
        self.DeviceDataList = []
        self.AliasReference = []
        self.DeviceLookUp = None
        self.DTSSourceDirectory = None
        self.DebugMode = False
        
    def ClearDTSData(self):
        self.DTSFileLines.clear()
        self.DTSContentList.clear()
    
    def ScanDTS(self):
        for dtsfile in  self.DTSFileList:
            self.DTSFileLines.clear()
            self.DTSContentList.clear()
            self.ReadFileToBuffer(dtsfile, self.DTSFileLines)
            self.ProcessDTSFile()                       

    
    def OpenDTS(self, DTSFile, DTSDir, DeviceLookUp):
            global DeviceReference
            self.DTSSourceDirectory = DTSDir
            self.DTSFileLines.clear()
            self.DTSContentList.clear()
            self.DeviceLookUp = DeviceLookUp

            if DeviceReference == None:
                DeviceReference = DeviceCatalogClass(DeviceLookUp)
                DeviceReference.UpdateDeviceCatalog()
            
            self.ReadFileToBuffer(DTSFile, self.DTSFileLines)

            if self.DebugMode == True:
                print("\n\n Processing DTS File ", DTSFile.getAbsolutePath())
            
            self.ProcessDTSFile()       
            self.PlatformDTSFileData.OpenDTS(DTSFile)
            
            for platDtsi in self.PlatformDTSIDataList:
              platDtsi.ConnectDataInfo(platDtsi.RootDataInfoList)

            self.PlatformDTSFileData.ConnectDataInfo(self.PlatformDTSFileData.RootDataInfoList)
            
            
            self.PlatformDTSFileData.TraceMap(self.PlatformDTSFileData.RootDataInfoList)
            
            self.PlatformDTSFileData.PrintDataInfo(self.PlatformDTSFileData.RootDataInfoList, 0)

            if self.DebugMode == True:
                print("Builder Output: ")
                for s in self.PlatformDTSFileData.BuilderOutput:
                    print(s)

            self.PlatformDTSFileData.GatherDeviceMap(self.PlatformDTSFileData.RootDataInfoList)

    
    def SearchDTS(self, searchString):
        self.PlatformDTSFileData.SearchDataInfo(self.PlatformDTSFileData.RootDataInfoList, searchString)
        for platDtsi in self.PlatformDTSIDataList:
          platDtsi.SearchDataInfo(platDtsi.RootDataInfoList, searchString)
    
    def ScanDevices(self):
        self.PlatformDTSFileData.SearchDevices(self.PlatformDTSFileData.RootDataInfoList)
    
    def ProcessDTSFile(self):
        startFlag = False
        brace_count = 0
        ProcessState = None
        ProcessList = []
        SaveTillEndBrace = False

        for i in range(0, len(self.DTSFileLines)):
            line = self.DTSFileLines[i]
            if "include" in line and "dtsi" in line:
                dtsiFile = line.replace("#include ", "").replace("\"", "")
                PlatformDTSI = PlatformDTSFileDataClass(self)
                PlatformDTSI.OpenDTSI(dtsiFile, self.DTSSourceDirectory)             
                self.PlatformDTSIDataList.append(PlatformDTSI)

            if "/ {" in line:
               startFlag = True
               brace_count += 1
               continue

            if startFlag == True:
               if "{" in line:
                   i = self.CaptureDataBetBrace(i, self.DTSContentList)
                   if i < 0:
                       break    
    
    def CaptureDataBetBrace(self, index, DTSContentList):
        Content = DTSContentClass()
        Content.ContentList.append(self.DTSFileLines[index])
        for j in range(index+1, len(self.DTSFileLines)):
            if "}" in self.DTSFileLines[j]:
                self.DTSContentList.append(Content)
                return j
            elif "{" in self.DTSFileLines[j]:
                j = self.CaptureDataBetBrace(j, Content.DTSContentList)
            else:
                Content.ContentList.append(self.DTSFileLines[j])

        return -1

    def ExtractData(self, pattern, fullString, s1, o1, s2, o2):
        return fullString.split(s1)[o1].split(s2)[o2]                
    
    def ReadFileToBuffer(self, dtsFile, lines):
        fileReader = open(dtsFile, "r")
        Filelines = fileReader.read().splitlines()
        fileReader.close()
        
        comment_line = False
        for line in Filelines:
            if len(line) > 0:
                if line.replace(" ", "").replace("\t", "").startswith("/*"):
                    if "*/" not in line:
                        comment_line = True
                        continue
                    else:
                      loop_end = False
                      index = 0
                      count = 0
                      while loop_end == False:
                        try:
                            index = line.index("/*", index)     
                        except ValueError:
                            break
                        index += 1
                        count += 1
 
                      if count == 1:
                        continue
                
                if comment_line == True:
                    if "*/" in line:
                        continue
                
                if line.replace(" ", "").replace("\t", "").startswith("//"):
                    continue
                
                line = line.replace("\t", "")
                line = line.replace("", "")
                lines.append(line)

class PlatformDTSFileDataClass:
    def __init__(self, dtsData): 
        self.PlatformDTSData = dtsData
        self.DTSFile = None
        self.DTSFileLines = []
        self.DTSContentList = []
        self.RootDataInfoList = []
        self.ObjAttribList = []
        self.ObjParamList = []
        self.AliasesData = None
        self.DTSAliasList = []
        self.DeviceDataList = []
        self.I2CMapDataList = []
        self.GPIOMapDataList = []
        self.LEDMapDataList = []
        self.IIOMapDataList = []
        self.PwmDataList = []
        self.TachoDataList = []
        self.EepromDataList = []
        self.SearchDataInfoList = []
        self.ControllerComponentDataList = []
        self.DeviceComponentDataList = []    
        self.DeviceModel = None
        self.DeviceCompatibleList = []
        self.AnalyzerMap = []
        self.BuilderOutput = []
        self.DebugMode = False
        self.ErrorState = False
        self.TotalI2CDevices = 0
        self.UnsupportedList = []
        
    def OpenDTSI(self, dtsiFile, DTSDir):
        self.DTSFile = dtsiFile

        DTSIFiles = []
        obj = os.scandir(DTSDir)
        for entry in obj:
            if dtsiFile in entry.name:
                DTSIFiles.append(entry)

        if len(DTSIFiles) > 0:
            self.ReadFileToBuffer(DTSIFiles[0], self.DTSFileLines)

        self.BuildDTSIFile()
        self.ProcessDTSIFile(self.RootDataInfoList)

    def PrintDeviceDataHeader(self):
        print("{: ^58} {: ^12} {: ^12} {: ^12} {: ^12} {: ^12} {: ^12} {: ^12} {: ^12} {: ^8}" .format("DTS Name", \
            "I2CBuss", \
            "I2CDevices", \
            "GPIOs", \
            "LEDs", \
            "IIODevices", \
            "Pwms", \
            "Tachos", \
            "Eeproms", \
            "UNSUPP"))

    def PrintDeviceData(self):
        if self.ErrorState == False: 
            print("{: ^58} {: ^12} {: ^12} {: ^12} {: ^12} {: ^12} {: ^12} {: ^12} {: ^12} {: ^8}" .format(self.DTSFile.name, \
                len(self.I2CMapDataList), \
                self.TotalI2CDevices, \
                len(self.GPIOMapDataList), \
                len(self.LEDMapDataList), \
                len(self.IIOMapDataList), \
                len(self.PwmDataList), \
                len(self.TachoDataList), \
                len(self.EepromDataList), \
                len(self.UnsupportedList)))
        
    def PrintDataInfo(self, dataInfoList, print_level):
        for dcc in dataInfoList:
            dcc.Print(print_level, dcc.DTSDataParent)
            if len(dcc.DataInfoList) > 0:
                self.PrintDataInfo(dcc.DataInfoList, print_level+1)
    
    def SearchDataInfo(self, dataInfoList, searchString):
        for dcc in dataInfoList:
            if len(dcc.ElementMap) > 0:
                for de in dcc.ElementMap:
                    if de.ElementString == None:
                        continue
            if len(dcc.DataInfoList) > 0:
                self.SearchDataInfo(dcc.DataInfoList, searchString)
    
    def SearchDevices(self, dataInfoList):
        for dcc in dataInfoList:
            if len(dcc.ElementMap) > 0:
                for de in dcc.ElementMap:
                    if de.ElementString == None:
                        continue
                    if de.ElementString.getKey() == "compatible":
                        self.DeviceDataList.append(dcc)

            if len(dcc.DataInfoList) > 0:
                self.SearchDevices(dcc.DataInfoList)

    def ConnectDataInfo(self, dataInfoList):
        for dcc in dataInfoList:
            dcc.ConnectAliases();            
            if len(dcc.DataInfoList) > 0:
                self.ConnectDataInfo(dcc.DataInfoList)
    
    def OpenDTS(self, dtsFile):
        self.DTSFile = Path(dtsFile)
        self.ReadFileToBuffer(dtsFile, self.DTSFileLines)
        self.BuildDTSIFile();        
        self.ProcessDTSIFile(self.RootDataInfoList);    
    
    def GetDataInfoForAlias(self, AliasName):
        for dtsalias in self.PlatformDTSData.AliasReference:
            if dtsalias.AliasName == AliasName:
                return dtsalias.AliasDataInfo
        
        return None   
    
    def CaptureDataBetBrace(self, index, DTSContentList, DataInfoList, Parent):
        MultiLine = []
        AliasFlag = False
        Content = DTSContentClass()
        DataInfo = DataInfoClass(self)
        Content.ContentList.append(self.DTSFileLines[index])
        DataInfo.ProcessDataHeader(self.DTSFileLines[index])
        DataInfo.Parent = Parent
        if DataInfo.FuncAlias != None or "aliases" in self.DTSFileLines[index]:
            Alias = DTSAliasClass()
            if "aliases" not in self.DTSFileLines[index]:
                AliasFlag = True
                Alias.AliasName = DataInfo.FuncAlias
                Alias.AliasDataInfo = DataInfo
                self.DTSAliasList.append(Alias)
                self.PlatformDTSData.AliasReference.append(Alias)
            else:
                Alias.AliasName = "Aliases"
                Alias.AliasDataInfo = DataInfo
                self.AliasesData = Alias
                self.PlatformDTSData.AliasReference.append(Alias)
        idx = 0
        for j in range(index+1, len(self.DTSFileLines)):
            if idx != 0:
                j = idx
                idx = 0
            if "}" in self.DTSFileLines[j]:
                DTSContentList.append(Content)
                DataInfoList.append(DataInfo)
                return j+1
            elif "{" in self.DTSFileLines[j]:
                idx = self.CaptureDataBetBrace(j, Content.DTSContentList, DataInfo.DataInfoList, DataInfo)       
                if idx >= len(self.DTSFileLines):
                    return idx
            else:
                if ";" in self.DTSFileLines[j]:
                    if len(MultiLine) > 0:
                        MultiLine.append(self.DTSFileLines[j])
                        Content.ContentList.append(self.DTSFileLines[j])            
                        DataInfo.ProcessMultiLine(MultiLine)
                        MultiLine.clear()
                    else:
                        DataInfo.ProcessDataInfo(self.DTSFileLines[j], AliasFlag)
                        Content.ContentList.append(self.DTSFileLines[j])

                else:
                    MultiLine.append(self.DTSFileLines[j])

        return -1

    def ExtractData(self, pattern, fullString, s1, o1, s2, o2):
        return fullString.split(s1)[o1].split(s2)[o2]
    
    def ReadFileToBuffer(self, dtsFile, lines):

        fileReader = open(dtsFile, "r")
        Filelines = fileReader.read().splitlines()
        fileReader.close()
        
        comment_line = False
        for line in Filelines:
            if len(line) > 0:                
                if line.replace(" ", "").replace("\t", "").startswith("/*"):
                    if "*/" not in line:
                        comment_line = True
                        continue
                    else:
                      loop_end = False
                      index = 0
                      count = 0
                      while loop_end == False:
                        try:
                            index = line.index("/*", index)                        
                        except ValueError:
                            break
                        index += 1
                        count += 1
 
                      if count == 1:
                        if line.endswith("*/"):
                            continue
                
                if comment_line == True:
                    if "*/" in line:
                        comment_line = False
                        continue
                
                if line.replace(" ", "").replace("\t", "").startswith("//"):
                    continue

                line = line.replace("\t", "")                
                if len(line) > 0:
                    lines.append(line.strip())
            
    def BuildDTSIFile(self):
        for i in range(0, len(self.DTSFileLines)):
            line = self.DTSFileLines[i]
            if "{" in line:
                i = self.CaptureDataBetBrace(i, self.DTSContentList, self.RootDataInfoList, None)
                if i < 0:
                    break
    
    def ProcessDTSIFile(self, dataInfoList):
        for dcc in dataInfoList:
            if dcc.FuncType == "/":
                self.DeviceModel = self.SearchElementMap(dcc.ElementMap, "model")
                self.DeviceCompatibleList = dcc.CompatibleList

            if len(dcc.ElementMap) > 0:  
                for p in dcc.ElementMap:
                    if p.ElementString == None:
                        continue
                    if p.ElementString.getKey() != None:
                        if p.ElementString.getKey() not in self.ObjAttribList:
                                self.ObjAttribList.append(p.ElementString.getKey())

            if len(dcc.ParamList) > 0:
                for p in dcc.ParamList:
                    if p != None:
                        if p not in self.ObjParamList:
                            self.ObjParamList.append(p)
            
            if len(dcc.DataInfoList) > 0:
                self.ProcessDTSIFile(dcc.DataInfoList)
    
    def ReturnFullString(self, FuncType, FuncAddress):
        if FuncAddress == None:
            return FuncType
        else:
            return FuncType+"@"+FuncAddress
    
    def TraceMap(self, dataInfoList):
        for dcc in dataInfoList:
            TraceString = ""
            TraceString = self.GetTraceMap(dcc)
            self.AnalyzerMap.append(TraceString)
            dcc.TraceMap = TraceString
            
            DeviceType = None
            if len(dcc.CompatibleList) > 0:
                for dtscc in dcc.CompatibleList:
                    for p in dtscc.CompatibleList:
                        DeviceJson = DeviceReference.SearchForDeviceType(p[1])
                        if DeviceJson != None:
                            DeviceType = DeviceJson.DeviceType
            
            if len(dcc.DataInfoList) > 0:
                self.TraceMap(dcc.DataInfoList)
    
    def GetTraceMap(self, dcc):
        TraceData = []
        dcc1 = dcc
        TraceData.append(self.ReturnFullString(dcc1.FuncType, dcc1.FuncAddress))
        if "&" in dcc.FuncType:
            for dac in dcc.DTSAliasReferenceList:
                if dac.AliasName == dcc.FuncType.replace("&", ""):
                    dcc1 = dac.AliasDataInfo

        if dcc1 != dcc:
            TraceData.append(self.ReturnFullString(dcc1.FuncType, dcc1.FuncAddress))

        dcc1 = dcc1.Parent
        while dcc1 != None:
            TraceData.append(self.ReturnFullString(dcc1.FuncType, dcc1.FuncAddress))
            if "&" in dcc1.FuncType:
                for dac in  dcc1.DTSAliasReferenceList:
                    if dac.AliasName == dcc1.FuncType.replace("&", ""):
                        dcc1 = dac.AliasDataInfo
                TraceData.append(self.ReturnFullString(dcc1.FuncType, dcc1.FuncAddress))

            dcc1 = dcc1.Parent

        TraceString = ""
        for i in range(len(TraceData) -1, 0, -1):
            if "/" not in TraceData[i]:
                TraceString += "/ "+TraceData[i].replace("&", "")
        
        TraceData.clear()
        return TraceString
    
    #####################################################################################

    def GetDataInfoListByElement(self, InputDataInfo, OutputDataInfo, element):
        for dic in InputDataInfo:
            if self.CheckElementKey(dic.ElementMap, element):
                OutputDataInfo.append(dic)

            if len(dic.DataInfoList) > 0:
                self.GetDataInfoListByElement(dic.DataInfoList, OutputDataInfo, element)
    
    def GetDataInfoList(self,FuncType, InputDataInfo, OutputDataInfo, Op):
        for dic in InputDataInfo:
            if Op == "EQUAL":
                if dic.FuncType == FuncType:
                    OutputDataInfo.append(dic)

            elif Op == "STARTSWITH":
                if dic.FuncType.startswith(FuncType):
                    OutputDataInfo.append(dic)
                                
            elif Op == "CONTAINS":
                if FuncType in dic.FuncType:
                    OutputDataInfo.append(dic)

            if len(dic.DataInfoList) > 0:
                self.GetDataInfoList(FuncType, dic.DataInfoList, OutputDataInfo, Op)
    
    def SearchElementDCC(self, dcc, key):
        if len(dcc.ElementMap) > 0:
            for element in dcc.ElementMap:
                if element.ElementString != None:
                    if element.ElementString.getKey() == key:
                        return element.ElementString.getValue()
        return None;        
    
    def SearchElementMap(self, ElementMap, key):
        for element in ElementMap:
            if element.ElementString != None:
                if element.ElementString.getKey() == key:
                    return element.ElementString.getValue()
        return None;        

    def SearchElementKeyPattern(self, ElementMap, Pattern):
        for element in ElementMap:
            if element.ElementString != None:
                if Pattern in element.ElementString.getKey():
                    return element.ElementString.getKey()
        return None;        
    
    def CheckElementKey(self, ElementMap, key):
        for element in ElementMap:
            if element.ElementString != None:
                if element.ElementString.getKey() == key:
                    return True
        return False;        
    
    def GatherI2CMapElements(self, dcc, I2CBus, Device):
        for dic in dcc.DataInfoList:
            ddc = I2CDeviceDataClass()
            ddc.DataInfo = dic
            ddc.Status = self.SearchElementDCC(dic, "status")
            ddc.CompatibleList = dic.CompatibleList
            ddc.DTSLabel = self.SearchElementDCC(dic, "label")
            ddc.SlaveAddress = dic.FuncAddress
            if I2CBus != None:
                self.TotalI2CDevices += 1
                I2CBus.DeviceList.append(ddc)
            if Device != None:
                self.TotalI2CDevices += 1
                Device.I2CSubDeviceList.append(ddc)
            DeviceType = None
            if len(dic.CompatibleList) > 0:
                for dtscc in dic.CompatibleList:
                    for p in dtscc.CompatibleList:
                        #print(p)
                        DeviceJson = DeviceReference.SearchForDeviceType(p[1])   
                        if DeviceJson != None:
                            DeviceType = DeviceJson.DeviceType
                            #System.out.printf("\n%s:(%s) - %s I2C Bus Class %s -> %s", ReturnFullString(dic.FuncType, dic.FuncAddress), DeviceJson.FileInfo, p.getValue(), DeviceJson.DeviceType, dic.TraceMap)
                        else:  
                            self.UnsupportedList.append(p)
                            if self.DebugMode == True:                         
                                print("\n%s:(NA)- %s I2C Bus Class NA -> %s" %(self.ReturnFullString(dic.FuncType, dic.FuncAddress), p[1], dic.TraceMap))
            else:
                #print("DEBUG 2")
                if self.DebugMode == True:                         
                    print("\n%s: NC--> %s" %(self.ReturnFullString(dic.FuncType, dic.FuncAddress), dic.TraceMap))

            if len(dic.CompatibleList) > 0:
                if len(dic.DataInfoList) > 0:
                    self.ControllerComponentDataList.append(dic)
                else:
                    self.DeviceComponentDataList.append(dic)

            if DeviceType != None:
                if "eeprom" in DeviceType:
                    eeprom = EepromDTSDataClass()
                    eeprom.DataInfo = dic
                    eeprom.I2CDevice = ddc
                    eeprom.Name = ddc.DTSLabel
                    self.EepromDataList.append(eeprom)
            
            if len(dic.DataInfoList) > 0:
                if DeviceType != None:
                    if "muxes" in DeviceType:                        
                        i2cBusData = I2CBusDataClass()
                        i2cBusData.DataInfo = dic
                        i2cBusData.BusId= dic.FuncType
                        i2cBusData.BusLevel = "0"
                        i2cBusData.BusName = "TBA"
                        i2cBusData.Status = self.SearchElementDCC(dcc, "status")
                        ddc.I2CSecBusList.append(i2cBusData)
                        self.GatherI2CMapElements(dic,i2cBusData, None)
                    elif "gpio" in DeviceType:                        
                        self.AddI2CElementToGPIOMap(dic)
                        self.GatherI2CMapElements(dic,None,ddc)
                    elif "adc" in DeviceType:
                        #print(("\n%s: I2C Bus Class %s -> %s" %(self.ReturnFullString(dic.FuncType, dic.FuncAddress), DeviceType, dic.TraceMap)))
                        self.GatherI2CMapElements(dic,None,ddc)
                    elif "pwm" in DeviceType:
                        #print(("\n%s: I2C Bus Class %s -> %s" %(self.ReturnFullString(dic.FuncType, dic.FuncAddress), DeviceType, dic.TraceMap)))
                        self.GatherI2CMapElements(dic,None,ddc)
                    elif "leds" in DeviceType:
                        #print(("\n%s: I2C Bus Class %s -> %s" %(self.ReturnFullString(dic.FuncType, dic.FuncAddress), DeviceType, dic.TraceMap)))
                        self.GatherI2CMapElements(dic,None,ddc)
                    elif "pmbus" in DeviceType:
                        #print(("\n%s: I2C Bus Class %s -> %s" %(self.ReturnFullString(dic.FuncType, dic.FuncAddress), DeviceType, dic.TraceMap)))
                        self.GatherI2CMapElements(dic,None,ddc)
                    else:
                        #print(("\n%s: I2C Bus Class %s -> %s" %(self.ReturnFullString(dic.FuncType, dic.FuncAddress), DeviceType, dic.TraceMap)))
                        self.GatherI2CMapElements(dic,None,ddc)
                else:
                    self.GatherI2CMapElements(dic,None,ddc)
    
    def AddI2CElementToGPIOMap(self, dcc):
        if "gpio-controller" in dcc.ParamList:            
            if self.CheckElementKey(dcc.ElementMap, "gpio-line-names"):
                #print("\n GPIO-lines-names %s" %dcc.FuncType)
                self.GatherGPIOMapElements(dcc, "gpio-line-names", "I2C", "gpio-controller")
            
            for dic in dcc.DataInfoList:
                if self.CheckElementKey(dic.ElementMap, "type"):
                    #print("\n type %s" %dcc.FuncType)
                    self.GatherGPIOMapElements(dic, "type", "I2C", "gpio-controller")
                else:
                    self.GatherGPIOMapElements(dic, "gpio", "I2C", "gpio-controller")
        else:   
            if self.DebugMode == True:          
                print("\n No GPIO Controller %s" %dcc.FuncType)    
        
    def GatherGPIOMapElements(self, dcc, Source, InterfaceType, ControllerType):
        if Source != None:
            if Source == "type":
                gpioData = GPIODTSDataClass()
                gpioData.InterfaceType = InterfaceType
                gpioData.ControllerType = ControllerType
                gpioData.DataInfo = dcc;           
                gpioData.CreateGPIOI2CExt("ExtType");            
                gpioData.GPIOI2CExt.ExtType.Reg = self.SearchElementMap(dcc.ElementMap, "reg")
                gpioData.GPIOI2CExt.ExtType.Type = self.SearchElementMap(dcc.ElementMap, "type")
                self.GPIOMapDataList.append(gpioData)
                return
            else:
                if self.CheckElementKey(dcc.ElementMap, "gpios"):
                    gpioData = GPIODTSDataClass()
                    gpioData.InterfaceType = InterfaceType
                    gpioData.ControllerType = ControllerType
                    gpioData.DataInfo = dcc;       
                    gpioData.CreateGPIOI2CExt("GPIOS")
                    gpios = self.SearchElementMap(dcc.ElementMap, "gpios")
                    linename = self.SearchElementMap(dcc.ElementMap, "line-name");                    
                    gpioData.GPIOI2CExt.GPIOLine.GPIOString = gpios
                    if linename == None:
                        linename = dcc.FuncType
                    
                    gpioData.GPIOI2CExt.GPIOLine.LineName = linename
                    elements = gpios.split(" ")
                    if len(elements) == 2:
                        gpioData.GPIOI2CExt.GPIOLine.LineID = elements[0]
                        gpioData.GPIOI2CExt.GPIOLine.defaultState = elements[1]
                    elif len(elements) == 3:
                        gpioData.GPIOI2CExt.GPIOLine.LineSource = elements[0]
                        gpioData.GPIOI2CExt.GPIOLine.LineID = elements[1]
                        gpioData.GPIOI2CExt.GPIOLine.defaultState = elements[2];                        
                    else:
                        if self.DebugMode == True:                         
                            print("\n GatherGPIOMapElements %s %s" %(gpios, linename))
                    
                    self.GPIOMapDataList.append(gpioData)
                    return

        if len(dcc.ElementMap) != 0:
            if self.CheckElementKey(dcc.ElementMap, "gpios"):
                # GPIO Line Information 
                gpios = self.SearchElementMap(dcc.ElementMap, "gpios")
                linename = self.SearchElementMap(dcc.ElementMap, "line-name")
                if linename == None:
                    linename = dcc.FuncType
                
                gpioData = GPIODTSDataClass()
                gpioData.Status = self.SearchElementMap(dcc.ElementMap, "status")
                gpioData.InterfaceType = InterfaceType
                gpioData.ControllerType = ControllerType
                gpioData.DataInfo = dcc;            
                gpioData.CreateGPIOLine()
                gpioData.GPIOLine.GPIOString = gpios
                gpioData.GPIOLine.LineName = linename
                elements = gpios.split(" ")
                if len(elements) == 2:
                    gpioData.GPIOLine.LineID = elements[0]
                    gpioData.GPIOLine.defaultState = elements[1]
                elif len(elements) == 3:
                    gpioData.GPIOLine.LineSource = elements[0]
                    gpioData.GPIOLine.LineID = elements[1]
                    gpioData.GPIOLine.defaultState = elements[2];                        
                else:
                    if self.DebugMode == True:                         
                        print("\n GatherGPIOMapElements %s %s" %(gpios, linename))

                self.GPIOMapDataList.append(gpioData)

            elif self.CheckElementKey(dcc.ElementMap, "gpio-line-names"):
                for p in dcc.ElementMap:
                    if len(p.DataTokenList) > 0:
                        if len(p.DataTokenList) == 1:
                            for sss in p.DataTokenList[0].Tokens:            
                                if self.DebugMode == True:                                             
                                    print("\n GatherGPIOMapElements (M): ", sss)
                        else:
                            # GPIO-line-Names 
                            for dtoken in p.DataTokenList:                                
                                if len(dtoken.Header) == 1:
                                    for k in range(0, len(dtoken.Tokens)):
                                        if len(dtoken.Tokens[k]) > 0 :
                                            gpioData = GPIODTSDataClass()
                                            gpioData.Status = self.SearchElementMap(dcc.ElementMap, "status")
                                            gpioData.InterfaceType = InterfaceType
                                            gpioData.ControllerType = ControllerType
                                            gpioData.DataInfo = dcc;            
                                            gpioData.CreateGPIOLine()
                                            gpioData.GPIOLine.LineID = dtoken.Header+str(k)
                                            gpioData.GPIOLine.LineName = dtoken.Tokens[k]
                                            gpioData.GPIOLine.LineSource = "BMC"
                                            self.GPIOMapDataList.append(gpioData)
                                elif "-" in dtoken.Header:
                                    StartRange = dtoken.Header.split("-")[0]
                                    EndRange = dtoken.Header.split("-")[1];     
                                    Prefix = StartRange[0:len(StartRange)-1]
                                    for k in range( 0, len(dtoken.Tokens)):
                                        if len(dtoken.Tokens[k]) > 0:
                                            gpioData = GPIODTSDataClass()
                                            gpioData.Status = self.SearchElementMap(dcc.ElementMap, "status")
                                            gpioData.InterfaceType = InterfaceType
                                            gpioData.ControllerType = ControllerType
                                            gpioData.DataInfo = dcc;            
                                            gpioData.CreateGPIOLine()
                                            gpioData.GPIOLine.LineID = Prefix+ str(k)
                                            gpioData.GPIOLine.LineName = dtoken.Tokens[k]
                                            gpioData.GPIOLine.LineSource = "BMC"
                                            self.GPIOMapDataList.append(gpioData)                                            
                    #elif len(p.MultiLineString) > 0:
                    #    for s in p.MultiLineString:
                            #print("DEBUG 7")
                            #print("\n GatherGPIOMapElements (SSS): %s " %s)
            else:   
                if self.DebugMode == True:              
                    print("\n GatherGPIOMapElements No Pattern %s" %(self.ReturnFullString(dcc.FuncType, dcc.FuncAddress)))
        else:
            if self.DebugMode == True: 
                print("\n GatherGPIOMapElements No Elements%s" %(self.ReturnFullString(dcc.FuncType, dcc.FuncAddress)))
        
        for dic in dcc.DataInfoList:
            self.GatherGPIOMapElements(dic, Source, InterfaceType, ControllerType)

    def GatherGPIOKeysMapElements(self, dcc, Source, InterfaceType, ControllerType):
        for dic in dcc.DataInfoList:
            if len(dic.ElementMap) > 0:
                if self.CheckElementKey(dic.ElementMap, "gpios"):
                    # GPIO Line Information 
                    gpios = self.SearchElementMap(dic.ElementMap, "gpios")
                    label = self.SearchElementMap(dic.ElementMap, "label")
                    linuxcode = self.SearchElementMap(dic.ElementMap, "linux,code")
                    if label == None:
                        label = dic.FuncType
                    
                    gpioData = GPIODTSDataClass()
                    gpioData.Status = self.SearchElementMap(dic.ElementMap, "status")
                    gpioData.InterfaceType = InterfaceType
                    gpioData.ControllerType = ControllerType;                    
                    gpioData.DataInfo = dic;            
                    gpioData.CreateGPIOKeys()
                    gpioData.GPIOKeys.Label = label;                    
                    gpioData.GPIOKeys.LinuxCode = linuxcode
                    elements = gpios.split(" ")
                    if len(elements) == 2:
                        if self.DebugMode == True:                         
                            print("\n GatherGPIOKeysMapElements Len 2 %s" %gpios)
                    elif len(elements) == 3:
                        gpioData.GPIOKeys.LineInfo.LineSource = elements[0]
                        gpioData.GPIOKeys.LineInfo.LineID = elements[1]
                        gpioData.GPIOKeys.LineInfo.defaultState = elements[2];                        
                    else:
                        if self.DebugMode == True: 
                            print("\n GatherGPIOKeysMapElements LEN Incorrect %s" %gpios)
                    
                    self.GPIOMapDataList.append(gpioData)
            else:
                if self.DebugMode == True: 
                    print("\n GatherGPIOKeysMapElements Empty Element Map")

    def GatherGPIOKeysPolledMapElements(self, dcc, Source, InterfaceType, ControllerType):        
        pollinterval = self.SearchElementMap(dcc.ElementMap, "poll-interval").replace("<", "").replace(">", "");        
        
        for dic in dcc.DataInfoList:
            if len(dic.ElementMap) > 0:
                if self.CheckElementKey(dic.ElementMap, "gpios"):
                    # GPIO Line Information 
                    gpios = self.SearchElementMap(dic.ElementMap, "gpios")
                    label = self.SearchElementMap(dic.ElementMap, "label")
                    linuxcode = self.SearchElementMap(dic.ElementMap, "linux,code")
                    if label == None:
                        label = dic.FuncType

                    gpioData = GPIODTSDataClass()
                    gpioData.Status = self.SearchElementMap(dic.ElementMap, "status")
                    gpioData.InterfaceType = InterfaceType
                    gpioData.ControllerType = ControllerType;                    
                    gpioData.DataInfo = dic;            
                    gpioData.CreateGPIOKeysPolled()
                    gpioData.GPIOKeysPolled.PollInterval = int(pollinterval.replace(';',""))
                    gpioData.GPIOKeysPolled.GPIOKeys.Label = label;                    
                    gpioData.GPIOKeysPolled.GPIOKeys.LinuxCode = linuxcode
                    elements = gpios.split(" ")
                    if len(elements) == 2:
                        if self.DebugMode == True:                         
                            print("\n GatherGPIOKeysPolledMapElements Len 2 %s" %gpios)
                    elif len(elements) == 3:
                        gpioData.GPIOKeysPolled.GPIOKeys.LineInfo.LineSource = elements[0]
                        gpioData.GPIOKeysPolled.GPIOKeys.LineInfo.LineID = elements[1]
                        gpioData.GPIOKeysPolled.GPIOKeys.LineInfo.defaultState = elements[2];                        
                    else:
                        if self.DebugMode == True: 
                            print("\n GatherGPIOKeysPolledMapElements LEN Incorrect %s" %gpios)

                    self.GPIOMapDataList.append(gpioData)
            else:
                if self.DebugMode == True: 
                    print("\n GatherGPIOKeysPolledMapElements Empty Element Map")

    def GatherLEDMapElements(self, dcc):
        for dic in dcc.DataInfoList:
            if len(dic.ElementMap) != 0:
                if  self.CheckElementKey(dic.ElementMap, "gpios"):
                    # GPIO Line Information 
                    gpios = self.SearchElementMap(dic.ElementMap, "gpios");                    
                    label = self.SearchElementMap(dic.ElementMap, "label");    
                    if "/*" in gpios:
                        gpios = gpios.replace(gpios[gpios.index("/*"):gpios.index("*/")+2],"")
                    if label == None:
                        label = dic.FuncType
                    
                    gpioData = GPIODTSDataClass()
                    gpioData.CreateLED()
                    gpioData.LED.Source = label
                    gpioData.LED.Status = self.SearchElementMap(dic.ElementMap, "status")
                    gpioData.DataInfo = dic;  
                    gpioData.LED.LineInfo.GPIOString = gpios
                    gpioData.LED.LineInfo.LineName = label
                    elements = gpios.split(" ")
                    if len(elements) == 2:
                        if self.DebugMode == True:                         
                            print("\n GatherLEDMapElements Len 2 %s" %gpios)
                    elif len(elements) == 3:
                        gpioData.LED.LineInfo.LineSource = elements[0]
                        gpioData.LED.LineInfo.LineID = elements[1]
                        gpioData.LED.LineInfo.defaultState = elements[2];                        
                                        
                    self.LEDMapDataList.append(gpioData)
            else:
                if self.DebugMode == True: 
                    print("\n GatherLEDMapElements Empty Element Map")

    def GatherIioHmomMapElements(self, dic):
        if len(dic.ElementMap) > 0:
            if self.CheckElementKey(dic.ElementMap, "io-channels"):                
                for p in dic.ElementMap:
                    if p.ElementString.getKey() == "io-channels":
                        if len(p.DataTokenList) > 0:
                            for dtoken in p.DataTokenList:
                                for k in range(0, len(dtoken.Tokens)):
                                    if dtoken.Tokens[k] == '':
                                        continue
                                    iiohwmon = IioHwmonDTSDataClass()                                    
                                    adctokens = dtoken.Tokens[k].replace("<", "").replace(">", "").replace(" &", "&").replace(";", "").split(" ")
                                    iiohwmon.ADCSource = adctokens[0]
                                    if len(adctokens) > 1:
                                        iiohwmon.Channel = adctokens[1]
                                    iiohwmon.DataInfo = dic
                                    self.IIOMapDataList.append(iiohwmon)
                        else:
                            adctokens = p.ElementString.getValue().replace("<", "").replace(">", "").replace(" &", "&").replace(";", "").split(" ")
                            iiohwmon = IioHwmonDTSDataClass()
                            iiohwmon.ADCSource = adctokens[0]
                            if len(adctokens) > 1:
                                iiohwmon.Channel = adctokens[1]
                            iiohwmon.DataInfo = dic
                            self.IIOMapDataList.append(iiohwmon)
        
        for dicc in dic.DataInfoList:
            self.GatherIioHmomMapElements(dicc)

    def GatherPwmTachoMapElements(self, dic):
        PwmPinDataList = []
        PwmDeviceInfo = None
        PwmInterfaceSource = None
        if len(dic.DTSAliasReferenceList) > 0:
            PwmTachoDeviceInfo = dic.DTSAliasReferenceList[0].AliasDataInfo
            PwmDeviceInfo = self.ReturnFullString(PwmTachoDeviceInfo.FuncType, PwmTachoDeviceInfo.FuncAddress)
            for dcomp in PwmTachoDeviceInfo.CompatibleList:
                for p in dcomp.CompatibleList:
                    PwmInterfaceSource = p[0]+":"+p[1]

        Status = self.SearchElementMap(dic.ElementMap, "status")
        pinctrl_names = self.SearchElementMap(dic.ElementMap, "pinctrl-names")
        if len(dic.ElementMap) > 0:
            for p in dic.ElementMap:
                if len(p.MultiLineString) > 0:
                    if p.ElementString.getKey().startswith("pinctrl-"):
                        for mString in p.MultiLineString:
                            mElements = mString.split(" ")
                            for i in range(0, len(mElements)):
                                if "&" in mElements[i]:
                                    PwmPinDataList.append(mElements[i].replace(";", "").replace(">","").replace("<", ""))

        for i in range(0, len(dic.DataInfoList)):
            pwmdts = PwmDTSDataClass()
            pwmdts.PwmID = dic.DataInfoList[i].FuncAddress
            pwm_string = self.SearchElementMap(dic.DataInfoList[i].ElementMap, "reg").replace("<", "").replace(">", "").replace(";", "").replace("0x","")
            pwm_idx = int(pwm_string, 16)
            pwmdts.PwmDataInfo = dic.DataInfoList[i]
            pwmdts.DeviceInfo = PwmDeviceInfo
            pwmdts.InterfaceSource = PwmInterfaceSource
            if len(PwmPinDataList) > 0:
                for pwmpindata in PwmPinDataList:
                    if str(pwm_idx) in pwmpindata:
                        pwmdts.PwmPinDataInfo = self.GetDataInfoForAlias(pwmpindata.replace("&",""))
                        break
            pwmdts.PWMName = "PWM-"+ self.ReturnFullString(dic.DataInfoList[i].FuncType, dic.DataInfoList[i].FuncAddress)
            FanDeviceInfo = self.SearchElementKeyPattern(dic.DataInfoList[i].ElementMap, "fan-tach")
            FanString = self.SearchElementMap(dic.DataInfoList[i].ElementMap, FanDeviceInfo)
            FanString = FanString[FanString.index("0x")]
            for s in FanString.split(" "):
                tachdts = TachDTSDataClass()
                tachdts.FanDeviceInfo = FanDeviceInfo
                tachdts.TachID = s
                tachdts.TachName = "Tach-"+s
                pwmdts.TachList.append(tachdts);                
                self.TachoDataList.append(tachdts)
            self.PwmDataList.append(pwmdts)
    
    def GatherDeviceMap(self, DataInfo):
        I2CList = []
        GPIOList = []
        GPIOKeysList = []
        GPIOKeysPolledList = []
        LedsList = []
        IioHwmonList = []
        PwmTachoList = []
        
        self.GetDataInfoList("&i2c", DataInfo, I2CList, "STARTSWITH")
        self.GetDataInfoList("&gpio", DataInfo, GPIOList, "STARTSWITH")
        self.GetDataInfoList("gpio-keys", DataInfo, GPIOKeysList, "EQUAL");        
        self.GetDataInfoList("gpio-keys-polled", DataInfo, GPIOKeysPolledList, "EQUAL")
        self.GetDataInfoList("leds", DataInfo, LedsList, "EQUAL")
        self.GetDataInfoListByElement( DataInfo, IioHwmonList, "io-channels")
        self.GetDataInfoList("&pwm_tacho", DataInfo, PwmTachoList, "EQUAL")
                
        if len(I2CList) > 0:
            for dic in I2CList:
                i2cBusData = I2CBusDataClass()
                i2cBusData.DataInfo = dic
                i2cBusData.BusId= dic.FuncType
                i2cBusData.BusLevel = "0"
                i2cBusData.BusName = "TBA"
                i2cBusData.Status = self.SearchElementDCC(dic, "status")                
                self.I2CMapDataList.append(i2cBusData)
                if len(dic.DataInfoList) > 0:
                    self.GatherI2CMapElements(dic, i2cBusData, None)
        
        if len(GPIOList) > 0:
            for dic in GPIOList:
                self.GatherGPIOMapElements(dic, None, "GPIO", "BMC")
        
        if len(GPIOKeysList) > 0:
            for dic in GPIOKeysList:
                self.GatherGPIOKeysMapElements(dic, None, "GPIO", "BMC")

        if len(GPIOKeysPolledList) > 0 :
            for dic in GPIOKeysPolledList:
                self.GatherGPIOKeysPolledMapElements(dic, None, "GPIO", "BMC")

        if len(LedsList) > 0:
            for dic in LedsList:
                self.GatherLEDMapElements(dic)

        if len(IioHwmonList) > 0:
            for dic in IioHwmonList:
                self.GatherIioHmomMapElements(dic)

        if len(PwmTachoList) > 0:
            for dic in PwmTachoList:
                self.GatherPwmTachoMapElements(dic)