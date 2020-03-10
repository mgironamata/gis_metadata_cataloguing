# Extract data from all datasets in ArcGIS geodatabase and save as CSV, where each row corresponds to one dataset's metadata.

import arcpy, os

arcpy.env.workspace = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\Jamaica_NSP_Master_Geodatabase_metadata_import_test.gdb"
xmlPath = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\4 Metadata_updated_xml_file"

fcs = arcpy.ListFeatureClasses()

XMLMissingFiles = []
UpdatedFiles = []

for fc in fcs[0:50]:
	fc_split = fc.split()
	fc_name = fc_split[-1]
	sourceXML = str(xmlPath)+"\\"+str(fc_name)+".xml"
	
	if os.path.exists(sourceXML):
    		arcpy.MetadataImporter_conversion(sourceXML,fc)
		UpdatedFiles.append(sourceXML)
		print "File updated: "+str(sourceXML)
	else:
		#pass
		print "WARNING - XML file missing: "+str(sourceXML)
		XMLMissingFiles.append(sourceXML) 
    
    #print "File processed: "+str(fc_name)
    
import csv

res = XMLMissingFiles
csvfile = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\5 Missing_xml_file_report\Feature_Classes_Not_Updated.csv"

#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in res:
        writer.writerow([val])    
		
		
res = UpdatedFiles
csvfile = r"J:\David Jarvis\JAMNSP Jamaica NSP\ArcGIS\Metadata\metadata_import_process\5 Missing_xml_file_report\Feature_Classes_Updated.csv"

#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in res:
        writer.writerow([val])    
