import json, sys
def read_DataFile(sRuta, sNombreArchivojson, sraisemsg):
    DictData={}
    try:
        with open(sRuta+sNombreArchivojson, mode ='r') as var_json:
            DictData=json.load(var_json)
            serror='NoError' 
    except:
        serror=(str(sraisemsg)) #str(sys.exc_info()[0]))
    DictData['serror']= serror
    return(DictData)

def write_DataFile(sRuta, sNombreArchivojson, sraisemsg, DictData):
    try:
        with open (sRuta+sNombreArchivojson, mode ='w') as var_json:
            json.dump(DictData , var_json)
            serror='NoError' 
    except:
        serror=(str(sraisemsg)) #str(sys.exc_info()[0]))
    return(serror)
    
    


   

