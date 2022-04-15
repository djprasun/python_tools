import re
import os
import nuke

nuke.scriptClear()
first = nuke.Panel("Prasun' team")

first.addEnumerationPulldown('Select show', 'PUF AAJ KAJ')


ret = first.show()

project = first.value('Select show')


if (project == 'KAJ'):
    print ('KAJ show selected')
    #path = "K:/workspace/animation/ep120"
    ep_list = ''
    path = "K:/workspace/animation/"
    for ep in os.listdir(path):
        
        if os.path.isdir(path):
            ep_folder = ep [:2].upper()
            #print (ep_folder) 
            if ep_folder == 'EP':
                
                print(ep)
                ep_list = ep_list+" "+ep
    #print(ep_list)          
    second = nuke.Panel("KAJ selected")

    second.addEnumerationPulldown('Select episode', ep_list)


    ret = second.show()
    
    
    ep = second.value('Select episode')
    
    anim_path = "K:/workspace/animation/"+ep
    
    playblast = 0
    counterx = 0
    countery = 0
    
    for dirpath, dirs, files in os.walk(anim_path): 
    
      for filename in files:
        fname = os.path.join(dirpath,filename)
        if fname.endswith('v00.mov'):
          playblast = playblast + 1
          counterx = counterx + 1
          readNode = nuke.nodes.Read()
          readNode.knob('file').fromUserText(fname)
          
          
          
          if counterx <= 50 :
              readNode.setXYpos( counterx*200 , countery )
              readNode.knob("label").setValue("[value first] - [value last]")
          
          else:
              countery = countery+600
              counterx = 1
              readNode.setXYpos( counterx*200 , countery )
              readNode.knob("label").setValue("[value first] - [value last]")


    mov = 0
    n = nuke.allNodes()
    for i in n:
        if i.Class() == "Read":
            oPath =  i["file"].value()
            oNewPath = re.sub('(animation)', 'compositing', oPath)
            original_string = "Python"
            sliced_string = oNewPath[:-28]
            print(sliced_string)
            ReadXPos = i['xpos'].value()
            ReadYPos = i['ypos'].value()
            
            
            #counter = 0
            for dirpath, dirs, files in os.walk(sliced_string): 
              for filename in files:
                fname = os.path.join(dirpath,filename)
                if fname.endswith('v00.mov'):
                    
                  readNode = nuke.nodes.Read()
                  readNode.knob('file').fromUserText(fname)
                  readNode.setXYpos( int(ReadXPos) , int(ReadYPos)+200 )
                  readNode.knob("label").setValue("[value first] - [value last]")
                  mov = mov + 1

                  
    dummy = nuke.nodes.Dot()
    nuke.delete(dummy)
    playblast_text = ("Number of playblast:"+str(playblast))
    mov_text = ("Number of Comp MOV:"+str(mov))
    nuke.message ("Number of playblast:"+str(playblast)+"\n" +"\nNumber of Comp MOV:"+str(mov))
    
    
    
elif  (project == 'AAJ'): 
    print ('AAJ show selected')
    ep_list = ''
    path = "A:/01prj/AAJ/prod/approved/"
    for ep in os.listdir(path):
        
        if os.path.isdir(path):
            ep_folder = ep [:2]
            #print (ep_folder) 
            if ep_folder == 'EP':
                
                print(ep)
                ep_list = ep_list+" "+ep
    #print(ep_list)          
    second = nuke.Panel("AAJ selected")

    second.addEnumerationPulldown('Select episode', ep_list)


    ret = second.show()
    
    
    ep = second.value('Select episode')
    anim_path = "A:/01prj/AAJ/prod/approved/"+ep+"/Animation/Approved"
    print(anim_path)
    
    counter = 0
    counterx = 0
    countery = 0
    check_seq = 10
    ext = (".mov", ".MOV")
    for file in os.listdir(anim_path):
        if file.endswith(tuple(ext)):
              print(os.path.join(anim_path, file))
              new_anim_path = os.path.join(anim_path, file)
              
              #file = os.path.basename(oPath).split("_")
              project = os.path.basename(file).split("_")[0]
              ep = os.path.basename(file).split("_")[1]
              seq = os.path.basename(file).split("_")[2]
              shot = os.path.basename(file).split("_")[3]
              dir = os.path.dirname(file)

              
              
              seq = os.path.basename(file).split("_")[2]
              counter = counter + 1
              counterx = counterx + 1
              print (file)
              print (seq)
              seqnum = seq [2:]
              print (seqnum)
              
              
              readNode = nuke.nodes.Read()
              readNode.knob('file').fromUserText(new_anim_path)
              
              countery = int(seqnum)
              
              if (check_seq != seqnum):
                counterx =  1
                check_seq = seqnum
              
              posx = counterx*200
              posy = int(countery*100)
              readNode.setXYpos( posx , posy )
              readNode.knob("label").setValue("[value first] - [value last]")
              
              comp_path = ("A:/01prj/AAJ/prod/shotpub/"+ep+"/"+seq+"/"+shot+"/lit_compout/sequence/mov/")
              new_file_name = (project+"_"+ep+"_"+seq+"_"+shot+"_left_compout.mov")
              print(comp_path)
              
              ReadXPos = posx
              ReadYPos = posy
              
              y = 0
              for dirpath, dirs, files in os.walk(comp_path): 
                      for filename in files:
                        fname = os.path.join(dirpath,filename)
             
                        if fname.endswith(new_file_name):
                          y = y + 200
                          readNode = nuke.nodes.Read()
                          readNode.knob('file').fromUserText(fname)
                          readNode.setXYpos( int(ReadXPos) , int(ReadYPos)+y )
                          readNode.knob("label").setValue("[value first] - [value last]")
              

                
     
    dummy = nuke.nodes.Dot()
    nuke.delete(dummy)
    nuke.message ("number of files:"+str(counter))
    #new_path = ("A:/01prj/AAJ/prod/shotpub/"+ep+"/"+seq+"/"+shot+"/lit_compout/sequence/mov/")
    #new_file_name = (project+"_"+ep+"_"+seq+"_"+shot+"_left_compout.mov")
        
elif  (project == 'PUF'): 
    print ('PUF show selected')
    ep_list = ''
    path = "P:/01prj/PUF/prod/approved/"
    for ep in os.listdir(path):
        
        if os.path.isdir(path):
            ep_folder = ep [:2]
            #print (ep_folder) 
            if ep_folder == 'EP':
                
                print(ep)
                ep_list = ep_list+" "+ep
    #print(ep_list)          
    second = nuke.Panel("PUF selected")

    second.addEnumerationPulldown('Select episode', ep_list)


    ret = second.show()
    
    
    ep = second.value('Select episode')
    anim_path = "P:/01prj/PUF/prod/approved/"+ep+"/Animation/Approved"
    print(anim_path)
    
    counter = 0
    counterx = 0
    countery = 0
    check_seq = 10
    for file in os.listdir(anim_path):
        if file.endswith(".mov") or file.endswith(".MOV"):
              print(os.path.join(anim_path, file))
              new_anim_path = os.path.join(anim_path, file)
              
              #file = os.path.basename(oPath).split("_")
              project = os.path.basename(file).split("_")[0]
              ep = os.path.basename(file).split("_")[1]
              seq = os.path.basename(file).split("_")[2]
              shot = os.path.basename(file).split("_")[3]
              dir = os.path.dirname(file)

              
              
              seq = os.path.basename(file).split("_")[2]
              counter = counter + 1
              counterx = counterx + 1
              print (file)
              print (seq)
              seqnum = seq [2:]
              print (seqnum)
              
              
              readNode = nuke.nodes.Read()
              readNode.knob('file').fromUserText(new_anim_path)
              
              countery = int(seqnum)
              
              if (check_seq != seqnum):
                counterx =  1
                check_seq = seqnum
              
              posx = counterx*200
              posy = int(countery*100)
              readNode.setXYpos( posx , posy )
              readNode.knob("label").setValue("[value first] - [value last]")
              
              comp_path = ("P:/01prj/PUF/prod/shotpub/"+ep+"/"+seq+"/"+shot+"/lit_compout/sequence/mov/")
              new_file_name = (project+"_"+ep+"_"+seq+"_"+shot+"_left_compout.mov")
              print(comp_path)
              
              ReadXPos = posx
              ReadYPos = posy
              
              y = 0
              for dirpath, dirs, files in os.walk(comp_path): 
                      for filename in files:
                        fname = os.path.join(dirpath,filename)
             
                        if fname.endswith(new_file_name):
                          y = y + 200
                          readNode = nuke.nodes.Read()
                          readNode.knob('file').fromUserText(fname)
                          readNode.setXYpos( int(ReadXPos) , int(ReadYPos)+y )
                          readNode.knob("label").setValue("[value first] - [value last]")
              

                
     
    dummy = nuke.nodes.Dot()
    nuke.delete(dummy)
    nuke.message ("number of files:"+str(counter))       
        
else:
    print ('No show selected')

