import nuke
import csv
import os

def createsticky():
    aaj_excel= 'P:\\01prj\\PUF\\prod\\shotpub\\Allotment\\Artist_Backup\\Prasun\\very imp_dont delete\\excel_conversion\\AAJ_POST_STATUS.csv'

    # Primaries
    red = "FF0000FF"
    green = "00FF00FF"
    blue = "0000FFFF"

    # Complimentary 
    cyan = "00FFFFFF"
    magenta = "FF00FFFF"
    yellow = "FFFF00FF"

    n = nuke.allNodes()
    for i in n:
            if i.Class() == "Read":
                oPath =  i["file"].value()
                ReadXPos = i['xpos'].value()
                ReadYPos = i['ypos'].value()
                #print(oPath)
                try:
                    project = os.path.basename(oPath).split("_")[0]
                    ep = os.path.basename(oPath).split("_")[1]
                    seq = os.path.basename(oPath).split("_")[2]
                    shot = os.path.basename(oPath).split("_")[3]
                    dir = os.path.dirname(oPath)

                    
                    with open(aaj_excel, mode ='r' ,) as this_csv_file:
                    
                        for row in csv.DictReader(this_csv_file,delimiter=','):
                           
                            #print('##'+row[1])
                            if row['Episode'].upper() == ep and row['SEQ'] == seq  and row['SHOT'] == shot :
                                #readNode = nuke.nodes.Read()
                                
                                frame_value = "[value first] - [value last]"
                                comp_status = "\nComp Status - " + row['COMP_STATUS']
                                final_status = "\nFinal Status - " + row['FINAL_STATUS']
                                comp_artist = "\nComp Artist - " + row['COMP_ARTIST']
                                i.knob("label").setValue(frame_value+ comp_status + final_status + comp_artist)

                                

                                if row['Type'].upper() == 'MASTER':
                                        stickyNode = nuke.nodes.StickyNote( label = 'MASTER', note_font_size = 20)
                                        stickyNode.setXYpos( int(ReadXPos) , int(ReadYPos)- 40 )
                                        
                                        if (project == 'aaj'):
                                            new_path = ("A:/01prj/AAJ/prod/shotpub/"+ep+"/"+seq+"/"+shot+"/lit_compout/static/jpg/")
                                            
                                            for dirpath, dirs, files in os.walk(new_path.lower()): 
                                              for filename in files:
                                                fname = os.path.join(dirpath,filename)
                                                counter = 0
                                                #ext = ['.jpg','.jpeg']
                                                if fname.lower().endswith('g'):
                                                  print(fname)
                                                  
                                                  readNode = nuke.nodes.Read()
                                                  readNode.knob('file').fromUserText(fname)
                                                  readNode.setXYpos( int(ReadXPos)+ counter+50, int(ReadYPos)- 100 )
                                                  counter = counter + 100
                                         
                                        if (project == 'puf'):
                                            new_path = ("P:/01prj/PUF/prod/shotpub/"+ep+"/"+seq+"/"+shot+"/lit_compout/static/jpg/")
                                            
                                            for dirpath, dirs, files in os.walk(new_path.lower()): 
                                              for filename in files:
                                                fname = os.path.join(dirpath,filename)
                                                counter = 0
                                                #ext = ['.jpg','.jpeg']
                                                if fname.lower().endswith('g'):
                                                  print(fname)
                                                  
                                                  readNode = nuke.nodes.Read()
                                                  readNode.knob('file').fromUserText(fname)
                                                  readNode.setXYpos( int(ReadXPos)+ counter, int(ReadYPos)- 100 )#counter = counter + 1
                                                  counter = counter + 100
                                
                except IndexError:
                    continue
createsticky()                    