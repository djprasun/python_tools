import re
import os

import nuke


def createmov():
    oReadNodes = nuke.selectedNodes('Read')

    for oReadNode in oReadNodes:
            oPath =  oReadNode["file"].value()
            ReadXPos = oReadNode['xpos'].value()
            ReadYPos = oReadNode['ypos'].value()
            oNewPath = re.sub('(animation)', 'compositing', oPath)
            original_string = "Python"
            sliced_string = oNewPath[:-28]

            file = os.path.basename(oPath).split("_")
            project = os.path.basename(oPath).split("_")[0]
            

            if (project == 'aaj'):
                ep = os.path.basename(oPath).split("_")[1]
                seq = os.path.basename(oPath).split("_")[2]
                shot = os.path.basename(oPath).split("_")[3]
                dir = os.path.dirname(oPath)
                new_path = ("A:/01prj/AAJ/prod/shotpub/"+ep+"/"+seq+"/"+shot+"/lit_compout/sequence/mov/")
                new_file_name = (project+"_"+ep+"_"+seq+"_"+shot+"_left_compout.mov")
                
                
                print(new_path)
                countery = 0
                for dirpath, dirs, files in os.walk(new_path): 
                      for filename in files:
                        fname = os.path.join(dirpath,filename)
                        shotseq = os.path.basename(oPath).split("_")[2]
                        seqnum = shotseq [2:]
                        print (seqnum) 
                        if fname.endswith(new_file_name):
                          countery = countery + 150
                          readNode = nuke.nodes.Read()
                          readNode.knob('file').fromUserText(fname)
                          readNode.setXYpos( int(ReadXPos) , int(ReadYPos)+countery )
                          readNode.knob("label").setValue("[value first] - [value last]")
                
            elif (project == 'kaj'):
                for dirpath, dirs, files in os.walk(sliced_string): 
                  for filename in files:
                    fname = os.path.join(dirpath,filename)
                    
                    if fname.endswith('v00.mov'):
                      #counter = counter + 1
                      readNode = nuke.nodes.Read()
                      readNode.knob('file').fromUserText(fname)
                      readNode.setXYpos( int(ReadXPos) , int(ReadYPos)+200 )
                      readNode.knob("label").setValue("[value first] - [value last]")
                      
            elif (project == 'puf'):
                ep = os.path.basename(oPath).split("_")[1]
                seq = os.path.basename(oPath).split("_")[2]
                shot = os.path.basename(oPath).split("_")[3]
                dir = os.path.dirname(oPath)
                new_path = ("P:/01prj/PUF/prod/shotpub/"+ep+"/"+seq+"/"+shot+"/lit_compout/sequence/mov/")
                new_file_name = (project+"_"+ep+"_"+seq+"_"+shot+"_left_compout.mov")
                
                
                print(new_path)
                countery = 0
                for dirpath, dirs, files in os.walk(new_path): 
                      for filename in files:
                        fname = os.path.join(dirpath,filename)
                        shotseq = os.path.basename(oPath).split("_")[2]
                        seqnum = shotseq [2:]
                        print (seqnum) 
                        if fname.endswith(new_file_name):
                          countery = countery + 150
                          readNode = nuke.nodes.Read()
                          readNode.knob('file').fromUserText(fname)
                          readNode.setXYpos( int(ReadXPos) , int(ReadYPos)+countery )
                          readNode.knob("label").setValue("[value first] - [value last]")

        
createmov()                  
                  

   