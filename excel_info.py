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

                    print (ep+seq+shot)
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

                                if row['FINAL_STATUS'] == 'DONE' :
                                        i.knob("tile_color").setValue(int(blue, 16))
                                        
                                
                                        
                                if row['FINAL_STATUS'] == 'INT CORR':
                                        i.knob("tile_color").setValue(int(yellow, 16))
                                        
                                if row['COMP_STATUS'] == '' and  row['FINAL_STATUS'] == '':
                                        i.knob("tile_color").setValue(int(red, 16))
                                        
                                if row['FINAL_STATUS'] == '' and row['COMP_STATUS'] != '':
                                        i.knob("tile_color").setValue(int(magenta, 16))
                                        
                                if row['COMP_STATUS'] == 'TO CHECK' and  row['FINAL_STATUS'] == '' :
                                        i.knob("tile_color").setValue(int(green, 16))
                                        
                                if row['COMP_STATUS'] == 'TO CHECK' and  row['FINAL_STATUS'] == 'INT CORR' :
                                        i.knob("tile_color").setValue(int(cyan, 16))

                                 
                                
                except IndexError:
                    continue
createsticky()                    