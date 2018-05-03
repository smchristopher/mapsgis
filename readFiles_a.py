import arcpy, os, zipfile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

ws = "X:/OpenDataSite/Data"
arcpy.env.workspace = ws
outPath = "C:/Users/smchristopher/Workspaces/zippedData"

def checkFolder(inpath):
    folder = os.path.split(inpath)
    tempPath = outPath + '//' + folder[1]
    if not os.path.exists(outPath + '//' + folder[1]):
        os.makedirs(tempPath)
        
    return tempPath

def zipShape(inpath,inShape,files,path,dataList):
    print('starting zip')
    zf = zipfile.ZipFile(inpath+'//'+inShape.split('.')[0]+'.zip', mode='w')
    for shape in files:
        fileSplit = shape.split('.')
        if (fileSplit[0] == inShape.split('.')[0]):
            print('writing file...')
            zf.write(path+'//'+shape,shape,compress_type=compression)             
    print('closing file')
    zf.close()
             
def inventory_data(workspace):
    dataList = open("C:/Users/smchristopher/Workspaces/zippedData/dataList.txt",'w')
    walk = arcpy.da.Walk(workspace,datatype="FeatureClass")

    for path, path_names, data_names in walk:
        for data_name in data_names:
            tempPath = checkFolder(path)
            try:
                dirFiles = os.listdir(path)
                print(path)
            except:
                dataList.write('\n\n\n\n\n\n')
                continue
            else:
                zipShape(tempPath,data_name,dirFiles,path,dataList)
                dataList.write(data_name + '\n')
                
    dataList.close()
    print('Done!')
    

def describe():
    dataList = open("C:/Users/smchristopher/Desktop/Scripts/dataList.txt",'r')
    fileTypes = open("C:/Users/smchristopher/Desktop/Scripts/classTypes.txt",'w')

    lines = dataList.readlines()
    
    for line in lines:
        desc = arcpy.Describe(line.strip())
        spatialRef = desc.spatialReference
        splitLine = line.split('\\')
        fileTypes.write(splitLine[6]+'\n')
        outfc = os.path.join(ws, splitLine[6])
        outCS = arcpy.SpatialReference('NAD 1983 UTM Zone 11N')
        arcpy.Project_management(line,outfc,outCS)
    fileTypes.close()

def main():
    #inDirectory = raw_input("Please input directory path: ")
    inDirectory = "Z:/GIS DATASETS/GIS LOCAL/Bryan"
    inventory_data(inDirectory)
    #describe()

main()


    
