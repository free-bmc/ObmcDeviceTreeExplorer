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
from pathlib import Path
from dtsexplorer_lib import PlatformDTSClass
from utils import progressbar

#OBMC_LINUX_SOURCE_DIR='/../../linux-dev-6.0'
OBMC_LINUX_SOURCE_DIR=None
DTSFile = None 
ArchList = []
ArchDTSList = []
DTSDir = None
DTSFilter = []
DeviceReferenceFile = None

def BuildArchList(archdir):
    global ArchDTSList

    obj = os.scandir(archdir)
    for entry in obj:
        if entry.is_dir():
            if entry.name == 'dts':
                ArchDTSList.append(entry)
            BuildArchList(entry)

def Initialize():
    global OBMC_LINUX_SOURCE_DIR
    global ArchList

    if OBMC_LINUX_SOURCE_DIR == None:
        OBMC_LINUX_SOURCE_DIR = os.environ.get('OBMC_LINUX_SOURCE_DIR')
    if OBMC_LINUX_SOURCE_DIR == None:
        print("DTS Explorer requires OpenBMC Linux Source Path")
        print("OBMC_LINUX_SOURCE_DIR NOT SET")        
        print("perform git clone https://github.com/openbmc/linux and point to the directory")
        print("Use export OBMC_LINUX_SOURCE_DIR=<Linux Root Directory Path>")
        print("Error: Unable to Initialize the tool ")
        return -1               

    print("Linux Source Reference Directory is ", OBMC_LINUX_SOURCE_DIR)
    
    BuildArchList(os.path.join(OBMC_LINUX_SOURCE_DIR,'arch'))
    for arch in ArchDTSList:
        ArchList.append(str(Path(arch).absolute()).replace(os.path.join(OBMC_LINUX_SOURCE_DIR,'arch'),"").replace('/boot/dts',''))

    return 0


from dtsexplorer_lib import DebugLevel

def CLIStart(ToolVersion):
    global DTSFile
    global DTSDir
    global DTSFilter
    global DeviceReferenceFile

    print("CLI started ...")
    print("type help to get started ...")
    while True:
        option = input("Device Tree CLI >> ")
        #print(option)
        if option == "quit":
            exit()
        elif option == "help":
            print("Commands and Options:")
            print("\tversion       <options>                Version Info ")
            print("\tdtsfile       <dtsfile>                Set DTS File ")
            print("\tlistarch                               List Arch Types")            
            print("\tsetarch       <arch-type>              Set Arch Type")    
            print("\tdevref        <file>                   Set Device Reference Json File")                        
            print("\tsetdbg                                  Set Debug ON/OFF toggle")
            print("\tscan                                   Start DTS Scan Arch Directory using filters")         
            print("\tscanfile      <file>                   Start DTS Scan of File ")         
            print("\tfilter        <filter1,...>            Set DTS File Filters separated by commas")
        elif option.startswith("version"):
            print(ToolVersion)
        elif option.startswith("dtsfile"):
            suboption = option.split(" ")
            dtsfile = None
            if len(suboption) == 2:
                try:
                    dtsfile = open(suboption[1], "r")
                except FileNotFoundError:
                    print("Wrong file or file path")
            DTSFile = dtsfile
        elif option.startswith("listarch"):            
            print("List of Architectures Found :")
            for ar in ArchList:
                print('\t', ar.replace('/',''))
            #print(archlist)
        elif option.startswith("setarch"):
            suboption = option.split(" ")
            if len(suboption) == 2:
                for ar in ArchList:
                    a = ar.replace('/','')
                    if suboption[1] == a:
                        arch_index = ArchList.index(ar)
                        DTSDir = ArchDTSList[arch_index]
                        break
                print("Set Architecture to ", Path(DTSDir).absolute())
        elif option.startswith("setdbg"):
            if DebugLevel == 0: 
                print("DEBUG MODE ON")
                DebugLevel = 1
            else: 
                print("DEBUG MODE OFF")
                DebugLevel = 0

        elif option.startswith("devref"):
            suboption = option.split(" ")
            DeviceReferenceFile = suboption[1]

        elif option.startswith("filter"):
            suboption = option.split(" ")
            if len(suboption) > 2:
                for i in range(2, len(suboption)):
                    DTSFilter.append(suboption[i])
        elif option.startswith("scanfile"):
            suboption = option.split(" ")
            DTSFile = Path(suboption[1])
            PlatDTS = PlatformDTSClass()
            PlatDTS.OpenDTS(DTSFile, DTSDir, DeviceReferenceFile)
            PlatDTS.PlatformDTSFileData.PrintDeviceDataHeader()
            PlatDTS.PlatformDTSFileData.PrintDeviceData()
        elif option.startswith("scan"):
            if DTSDir == None:
                print("Error: Architecture is Not Set")
                continue

            obj = os.scandir(DTSDir)
            DTSFileList = []            
            PlatformDTSList = []
            for entry in obj:
                if entry.name.endswith('.dts'):
                    #print(entry.name)
                    DTSFileList.append(entry)
            
            for i in progressbar(range(len(DTSFileList)), "Scanning DTS Files : ", 100):
                    platDTS = PlatformDTSClass()
                    platDTS.OpenDTS(DTSFileList[i], DTSDir, DeviceReferenceFile)
                    PlatformDTSList.append(platDTS)
            PlatformDTSList[0].PlatformDTSFileData.PrintDeviceDataHeader()
            for pdts in PlatformDTSList:
                pdts.PlatformDTSFileData.PrintDeviceData()



