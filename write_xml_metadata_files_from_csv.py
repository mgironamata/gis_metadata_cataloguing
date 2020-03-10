#Write ArcGIS metadata XML files based on metadata information from CSV files, where each column corresponds to a different GIS dataset. 

#coding: utf-8

#PART 0 - IMPORT MODULES

import sys
import glob
import os
import numpy as np
import xml.etree.ElementTree as ET
from lxml import etree

#import arcpy
import csv
import tempfile
import codecs
import cStringIO
import time
from xml.etree.ElementTree import ElementTree


#PART 1 - DECLARE INPUT FILES

#csvFileName = input("Enter input CSv file path preceded by the letter r (e.g., r\"C:\Users\...\"): ")
#xmlInputPath = input("Enter input XMLs directory path preceded by the letter r (e.g., r\"C:\Users\...\"): ")
#xmlOutputPath = input("Enter output XMLs directory path preceded by the letter r (e.g., r\"C:\Users\...\"): ")

#TEST WITH MGM SAMPLE FILES 
#csvFileName = r"C:\Temp_Jamaica\DN_GDB\MGM_local_GDB\Template_metadata_import_sheet_MGM.csv"
#xmlInputPath = r"C:\Temp_Jamaica\DN_GDB\MGM_local_GDB\Output_XML"
#xmlTempPath = r"C:\Temp_Jamaica\DN_GDB\MGM_local_GDB\Temp_XML"
#xmlOutputPath = r"C:\Temp_Jamaica\DN_GDB\MGM_local_GDB\Updated_XML"

#TEST WITH MGM SAMPLE FILES 
csvFileName = r"C:\Users\marcg\Dropbox\GWP\Temp_Jobs\Jamaica NSP\metadata_import_process\1 Python_CSV_Input\Output to python from Combined MGM.csv"
xmlInputPath = r"C:\Users\marcg\Dropbox\GWP\Temp_Jobs\Jamaica NSP\metadata_import_process\2 Orginal_xml_files"
xmlTempPath = r"C:\Users\marcg\Dropbox\GWP\Temp_Jobs\Jamaica NSP\metadata_import_process\3 Temp_metadata_xml_file"
xmlOutputPath = r"C:\Users\marcg\Dropbox\GWP\Temp_Jobs\Jamaica NSP\metadata_import_process\4 Metadata_updated_xml_file"

#TEST WITH DN SAMPLE FILES  
#csvFileName = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\1 Python_CSV_Input\Output to python_V2.csv"
#xmlInputPath = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\2 Orginal_xml_files"
#xmlTempPath = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\3 Temp_metadata_xml_file"
#xmlOutputPath = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\MGM_TEMP_Metadata_updated_xml_file"

#xmlOutputPath = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\4 Metadata_updated_xml_file"

#xmlInput = r"C:\Users\marcg\Dropbox\GWP\Temp_Jobs\Jamaica NSP\Python_testing\from DN\ISO_template_feature.xml"
#xmlOutputPath = r"C:\Users\marcg\Dropbox\GWP\Temp_Jobs\Jamaica NSP\Python_testing\xml_output"

csvFileName.replace("\\","\\\\")
xmlInputPath.replace("\\","\\\\")
xmlTempPath.replace("\\","\\\\")
xmlOutputPath.replace("\\","\\\\")


#PART 2 - DEFINE DELIMITER FOR CSV FILE 

delimiter = "," # "\t" "|" # delimiter used in the CSV file(s)


#PART 3 - LOOP OVER CSV FILE LINES (TO GENERATE XML FILE NAMES) & RETRIEVE CSV HEADERS (XML ELEMENTS)

csvFile = open(csvFileName, 'rb')
csvFileRead = csv.reader(csvFile)
 
line_count = 0
csvHeaders = []
csvData = []
xmlFileNames = []

for line in csvFileRead:
    
    if line_count == 0:
        csvHeaders=line[1:]
    elif line_count == 1:
        pass
    else:
        #print len(line)
        xmlPathName = line[0]
        xmlPathName = xmlPathName + '.xml'
        xmlFileName = xmlPathName.split("\\")
        xmlFileName = xmlFileName[-1]                  
        #xmlFile = xmlFileName[0:-4] + '.xml'
        
        xmlFileNames.append(xmlFileName)
        csvData.append(line[1:])
        #print xmlFileName
        #print xmlPathName
        #print line[1:]
        #print "\n"
        
    line_count += 1
    
#for 
#tags = csvData.pop(0).strip().replace(', ','<;;;>').split(delimiter)
#for row in csvData:
    #rowencoded = row.encode('ascii')
    #rowData = rowencoded.replace(', ','<;;;>').split(delimiter)
    #print len(rowData)


# PART 4 - UPDATE XML FILES TO INCLUDE REQUIRED TREE STRUCTURE AND SAVE TEMPORARY XML FILES 

MissingFiles = []
line_count = 0

total_tic = time.clock()

for line in csvData:
    
    tic = time.clock()
    
    xmlInput = xmlInputPath + "\\" + str(xmlFileNames[line_count])
    #print xmlInput
    
    if os.path.exists(xmlInput):
    
        tree = etree.parse(xmlInput)
        root = tree.getroot()

        #root.tag
        #print "xmlInput:" + str(xmlInput)

        save_count = 0
        e_count = 0

        for h in csvHeaders: 

            h_element_split = h.split("/")
            #print h_element_split
            #h_element_name = h_element_split[-1]


            for i in range(0,len(h_element_split)):

                h_element_name = h_element_split[i]
                h_element_name_split = h_element_name.split("_")
                h_element_name = h_element_name_split[0]

                #print h_element_name

                if i == 0:
                    h_element_path = "/metadata"
                    #print "metadata = " + str(h_element_path)
                    if i == len(h_element_split)-1:
                        h_element_name = h_element_name#[:-4]
                    else:
                        pass                        
                elif i == len(h_element_split)-1:
                    #print i
                    h_element_path = "/".join(h_element_split[:i])
                    h_element_path = "/metadata/" + str(h_element_path)
                    h_element_name = h_element_name#[:-4]
                else:
                    h_element_path = "/".join(h_element_split[:i])
                    h_element_path = "/metadata/" + str(h_element_path)

                h_element_fullpath = str(h_element_path)+"/"+str(h_element_name)

                #print "HH = " + str(h_element_path)
                #print "EE = " + str(h_element_name)
                #print "FP = " + str(h_element_fullpath)
                #print i

                #len_h_element_name = len(h_element_name)
                #h_element_path = "/metadata/" + str(h[:-len_h_element_name])
                #h_element_name = h_element_name[:-4]
                #print h
                #print "Element = " + str(element_split)

                for e in root.iter():      
                    e_path = tree.getpath(e)
                    #e_elementpath = tree.getelementpath(e)
                    e_elementpath = tree.getpath(e)
                    #print "E =" + str(e_elementpath)
                    #print "H =" + str(h_element_path)
                    if str(e_elementpath) == h_element_fullpath:
                        #print "EXISTING\n"
                        break       
                else:
                    for e2 in root.iter():
                        e_elementpath = tree.getpath(e2)
                        #print "EE_1 = " + str(e_elementpath)
                        #print "HH_1 = " + str(h_element_path)
                        if str(e_elementpath) == h_element_path:
                            etree.SubElement(e2,str(h_element_name))
                            #print "FP =" + str(h_element_fullpath)
                            #print "UPDATED\n"
                            #print(etree.tostring(e, pretty_print=True))
                            #print "\n"
                            break
                    else:
                        print "ERROR\n" 

            #h_count +=1

        #for e3 in root.iter():
        #    e_path = tree.getpath(e3)
        #    print e_path

        tree = etree.ElementTree(root)                   

        outFilePath = str(xmlTempPath) + "\\" + str(xmlFileNames[line_count])    

        outFile = open(outFilePath, 'w')
        tree.write(outFile,encoding="UTF-8", xml_declaration=True, method="xml")
        #tree_tostring = etree.tostring(tree, xml_declaration=True)
        #tree_tostring.write(outFile)
        outFile.close()

        toc = time.clock()
        elapsed = toc-tic

        #print outFilePath  
        print "File No." + str(line_count+1) + " | Filename: " + str(xmlFileNames[line_count]) + " | Run time: " + str(elapsed)
        
    else:
        print "File missing: " + str(xmlInput)
        MissingFiles.append(xmlInput)
        
    line_count += 1
    
    
total_toc = time.clock()    
total_elapsed = total_toc - total_tic

print "\n" + "Number of XML files created: " + str(line_count) + " | Total run time: " + str(total_elapsed)  


# PART 5 - NESTED LOOPS OVER: I) CSV FILE LINES, II) MASTER XML ELEMENT STRUCTURE & III) CSV HEADERS; TO FILL AND GENERATE XML FILES  

MissingFiles_v2 = []
line_count = 0

total_tic = time.clock()

for line in csvData:
        
    tic = time.clock()
    
    xmlInput = xmlTempPath + "\\" + str(xmlFileNames[line_count])
    #print xmlInput
    
    if os.path.exists(xmlInput):
    
        tree = etree.parse(xmlInput)
        root = tree.getroot()

        #root.tag
        #print "xmlInput:" + str(xmlInput)

        save_count = 0
        e_count = 0

        h_count=-1
        for h in csvHeaders: 
            h_count=h_count+1

            h_split = h.split("_")
            #print h_split

            for e in root.iter():      
                e_path = tree.getpath(e)
                #e_elementpath = tree.getelementpath(e)
                e_elementpath = tree.getpath(e)
                #print "e_path:" +str(e_path)
                #print "e_elementpath:" +str(e_elementpath)
                #print "\n"

                #e.text = ""
                #e.tail = ""
                #d = e.attrib
                #for key in d:
                    #d[key]=""

                #e_count = e_count + 1

                e_elementpath_len = len(str(e_elementpath)+"_")-10

                #print "EE =" + str(e_elementpath)
                #print "HH =" + "/metadata/"+str(h)#[:e_elementpath_len])



                #if str(e_elementpath)+"_" == "/metadata/" + str(h[:e_elementpath_len]):
                if str(e_elementpath) == "/metadata/" + str(h_split[0]):
                    #print e_elementpath
                    #print h_split
                    #print "FOUND"

                    #print h_split[1]

                    if h_split[1] == "tex":
                        #print "h: "+str(h)
                        #print "newtext:"+str(line[h_count])
                        e.text = line[h_count]
                        #print "oldtext:"+str(e.text)
                        if e.tag == "keyword2":
                            e.tag = "keyword"
                            #print e.tag
                        else:
                            pass
                    elif h_split[1] == "tag":
                        #e.tag = line[h_count]
                        #print "tag:"+str(e.tag)
                        pass
                    elif h_split[1] == "tai":
                        e.tail = line[h_count]
                        #print "tail:"+str(e.tail)
                    elif h_split[1] == "att":
                        #print "ATT"
                        d = e.attrib 
                        #print "att:"+str(d)
                        for key in d:
                            #if key == "value":
                                #print type(d[key])
                                #print d[key]
                                #pass
                            #else:
                                #pass
                            #print h_split[2]
                            if key == h_split[2]:
                                if key == "value":
                                    #print "Updated existing key: "+str(d)
                                    #print line[h_count]
                                    numformat = float(line[h_count])
                                    d[key]="009"#'"'+str("%03d"%numformat)+'"'
                                    #d[key]=line[h_count]
                                    #print d[key]
                                    #print type(d[key])
                                else:
                                    d[key]=line[h_count]
                                    #print "Updated existing key: "+str(d)
                                #print e.attrib
                                break
                        else:
                            key = h_split[2]
                            if key == "value":
                                #print line[h_count]
                                numformat = float(line[h_count])
                                d[key]="009"#'"'+str("%03d"%numformat)+'"'
                                #d[key]=line[h_count]
                                #print "Updated new key: "+str(d)
                                #print d[key]
                                #print type(d[key])
                            else:
                                d[key] = line[h_count]
                                #print "Updated new key: "+str(d)
                            #print d
                    else:
                        #print e_elementpath
                        #print h
                        print "ERROR1\n" # flag
                        pass
                    break  

            else:
                print "ERROR2\n"
                #print "Element: "+str(e_elementpath)
                print "CSV field:"+"/metadata/" + str(h) 
                pass

        outFilePath = str(xmlOutputPath) + "\\" + str(xmlFileNames[line_count])    

        outFile = open(outFilePath, 'w')
        tree.write(outFile,encoding="UTF-8", xml_declaration=True, method="xml")
        #tree.write(outFile,encoding="ascii", xml_declaration=True, method="xml")
        #tree_tostring = etree.tostring(tree, xml_declaration=True)
        #tree_tostring.write(outFile)
        outFile.close()

        toc = time.clock()
        elapsed = toc-tic

        #print outFilePath  
        print "File No." + str(line_count+1) + " | Filename: " + str(xmlFileNames[line_count]) + " | Run time: " + str(elapsed)
    
    else:
        MissingFiles_v2.append(xmlInput)
        
    line_count += 1
    
total_toc = time.clock()    
total_elapsed = total_toc - total_tic

print "\n" + "Number of XML files created: " + str(line_count) + " | Total run time: " + str(total_elapsed)  


import csv

res = MissingFiles
csvfile = r"C:\Users\marcg\Dropbox\GWP\Temp_Jobs\Jamaica NSP\metadata_import_process\5 Missing_xml_file_report\XML_Files_Not_Updated.csv"

#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in res:
        writer.writerow([val])    

