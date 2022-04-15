import re
import os
import glob
#import import_comp_4rm_playblast
import nuke



    
def createanim(): 


     
    path = "A:/01prj/AAJ/prod/approved/EP722/Animation/Approved"
    #kim = 'K:/workspace/animation/'
    #txt = nuke.getInput('Which episode?', 'ep120')

    #path = '"'+kim+txt+'"'
    counter = 0
    counterx = 0
    countery = 0
    check_seq = 010
    for file in os.listdir(path):
        if file.endswith(".mov"):
              print(os.path.join(path, file))
              new_file_path = os.path.join(path, file)
              shotseq = os.path.basename(file).split("_")[2]
              counter = counter + 1
              counterx = counterx + 1
              print (file)
              print (shotseq)
              seqnum = shotseq [2:]
              print (seqnum)
              
              
              readNode = nuke.nodes.Read()
              readNode.knob('file').fromUserText(new_file_path)
              
              countery = int(seqnum)
              
              if (check_seq != seqnum):
                counterx =  1
                check_seq = seqnum
              
              readNode.setXYpos( counterx*150 , int(countery*100) )
              readNode.knob("label").setValue("[value first] - [value last]")
          
           
              
              
              

    nuke.message ("number of files:"+str(counter))



    
createanim()  




   