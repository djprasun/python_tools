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
    # open the file in read mode
    filename = open(aaj_excel, 'r')
     
    # creating dictreader object
    file = csv.DictReader(filename,delimiter=',')
     
     
    
    artist = []

    for col in file:
        artist.append(col['COMP_ARTIST'])

    
    mylist = list(set(artist))
    artist_list = ''
    for artist in mylist:
        artist_list = artist_list+" "+artist
        print(artist)
      
    first = nuke.Panel("Artist's name")

    first.addEnumerationPulldown('Select artist', artist_list)


    ret = first.show()

    artist_name = first.value('Select artist')
    # extract the variables you want
    
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

                                

                                if row['COMP_ARTIST'] == artist_name:
                                        stickyNode = nuke.nodes.StickyNote( label = artist_name, note_font_size = 30)
                                        stickyNode.setXYpos( int(ReadXPos) , int(ReadYPos)- 40 )
                                        
                                        
                                        
                                
                except IndexError:
                    continue
                    