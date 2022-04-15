
import os
import re
import shutil
import nuke
import getpass
import time
import csv

def make():
    shot_maker = nuke.Panel('Shot maker')
    shot_maker.addFilenameSearch('Parent nuke file', 'Search parent .nk')
    shot_maker.addClipnameSearch('Child shot playblast', 'Search anim .mov')
    shot_maker.addSingleLineInput('Version', 'V001')
    ret = shot_maker.show()
    child = shot_maker.value('Child shot playblast')
    parent = shot_maker.value('Parent nuke file')
    version = shot_maker.value('Version')

    child_project = os.path.basename(child).split("_")[0]
    child_ep = os.path.basename(child).split("_")[1]
    child_seq = os.path.basename(child).split("_")[2]
    child_shot = os.path.basename(child).split("_")[3]
    child_dir = os.path.dirname(child)

    parent_project = os.path.basename(parent).split("_")[0]
    parent_ep = os.path.basename(parent).split("_")[1]
    parent_seq = os.path.basename(parent).split("_")[2]
    parent_shot = os.path.basename(parent).split("_")[3]
    parent_dir = os.path.dirname(parent)



    #create folder
    create = "P:\\01prj\\PUF\\prod\\shotpub\\"+child_ep+"\\"+child_seq+"\\"+child_shot+"\\lit_compout\\sequence\\source\\"

    nuke_file = "puf_"+child_ep+"_"+child_seq+"_"+child_shot+"_lit_compout_sequence_source_"+version+".nk"
    comp_path = create + nuke_file
    #write_out = "P:\01prj\PUF\prod\shotpub\EP316\SQ020\SH180\lit_compout\sequence\source\puf_EP316_SQ020_SH180_lit_compout_sequence_source_V001.nk"
    if os.path.exists(comp_path):
        #nuke.message ("File exist! Don't worry, it will be moved to backup folder.")
        backup = create + "backup\\"
        if not os.path.exists(backup):
            os.makedirs(backup)


        shutil.copy(comp_path, backup)

        #if not nuke.ask(nuke_file+ ' exist! Do you want to overwrite?'):
        #    version = nuke.getInput('Version', 'V002')
        #    comp_path = create + "puf_"+child_ep+"_"+child_seq+"_"+child_shot+"_lit_compout_sequence_source_"+version+".nk"
    #nuke.message (child_ep+"_"+child_seq+"_"+child_shot+" will be created. Sit back and relax.")
    # path exists

    if not os.path.exists(create):
        os.makedirs(create)
    print(comp_path)

    #copy parent
    shutil.copy(parent, comp_path)
    #create user log
    import time
    username = getpass.getuser()
    time = time.ctime()
    date = time[:10]
    clock = time[11:20]
    year = time[20:]
    import csv
    csv_file = r"P:\01prj\PUF\prod\shotpub\Allotment\Artist_Backup\Prasun\very imp_dont delete\logs\artist_log.csv"

    fields=[username,child_ep,child_seq,child_shot,date,clock,year]
    # read header automatically

    with open(csv_file, 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(fields)



    #import render layer file
    nuke.scriptClear()
    nuke.knob("root.fps","25")
    nuke.knob("root.format","HD_1080")
    shot_folder = '''P:\\01prj\\PUF\\prod\\shotpub\\'''+child_ep+'''\\'''+child_seq+'''\\'''+child_shot
    counterx = 0
    countery = 1
    for shot, sub_dir, files in os.walk(shot_folder):
        for layers in sub_dir:
            if  layers == 'v000' or layers == 'V000':

                folder = (shot+'\\'+layers)
                
                try:
                    for seq in nuke.getFileNameList(folder):
                        render_file = folder +'\\'+seq
                        print (render_file)
                        for files in nuke.getFileNameList(render_file):
                            counterx = counterx + 1
                            posx = counterx*400
                            posy = int(countery*100)

                            for_read = render_file+'\\'+files
                            readNode = nuke.createNode('Read')
                            readNode.setXYpos( posx , posy )
                            readNode.knob('file').fromUserText(for_read)
                            ReadXPos = readNode['xpos'].value()
                            ReadYPos = readNode['ypos'].value()
                            stickyNode = nuke.nodes.StickyNote( label = seq, note_font_size = 40)
                            stickyNode.setXYpos( int(ReadXPos) , int(ReadYPos)- 80 )
                        
                except:
                        render_file = folder +'\\'
                        
                        for files in nuke.getFileNameList(render_file):
                            counterx = counterx + 1
                            posx = counterx*400
                            posy = int(countery*100)

                            for_read = render_file+'\\'+files
                            readNode = nuke.createNode('Read')
                            readNode.setXYpos( posx , posy )
                            readNode.knob('file').fromUserText(for_read)
                            ReadXPos = readNode['xpos'].value()
                            ReadYPos = readNode['ypos'].value()
                            stickyNode = nuke.nodes.StickyNote( label = files, note_font_size = 40)
                            stickyNode.setXYpos( int(ReadXPos) , int(ReadYPos)- 80 )
    #write node
    mov_out = shot_folder + "\lit_compout\sequence\mov\puf_"+child_ep+"_"+child_seq+"_"+child_shot+"_lit_compout_sequence_mov_"+version+"\puf_"+child_ep+"_"+child_seq+"_"+child_shot+"_left_compout.mov"
    dummy = nuke.nodes.Dot()
    nuke.delete(dummy)

    writeNode = nuke.nodes.Write()
    writeNode.setXYpos((posx/2) , (posy+500) )
    writeNode.knob('file').fromUserText(mov_out)
    writeNode.knob('channels').setValue('rgba')
    writeNode.knob('file_type').setValue('mov')
    writeNode.knob('meta_codec').setValue('ap4h')
    writeNode.knob('mov64_codec').setValue('ap4h')
    writeNode.knob('mov64_bitrate').setValue(20000)
    writeNode.knob('mov64_bitrate_tolerance').setValue(40000000)
    writeNode.knob('mov64_quality_min').setValue(2)
    writeNode.knob('mov64_quality_max').setValue(31)
    writeNode.knob('mov64_gop_size').setValue(12)
    writeNode.knob('mov64_b_frames').setValue(0)
    writeNode.knob('create_directories').setValue('true')
    writeNode.knob('checkHashOnRead').setValue('false')
    writeNode.knob('version').setValue(82)
    writeNode.knob('label').setValue(child_ep+"_"+child_seq+"_"+child_shot+"_MOV")
    writeNode.knob('tile_color').setValue(0xffffff)
    writeNode.knob('note_font_size').setValue(22)
    writeNode.knob('mov64_b_frames').setValue(0)
    stickyNode = nuke.nodes.StickyNote( label = ("WRITE NODE FOR "+child_ep+"_"+child_seq+"_"+child_shot), note_font_size = 50)
    stickyNode.setXYpos((posx/2) , (posy+600) )


    pre_comp = create + "puf_"+child_ep+"_"+child_seq+"_"+child_shot+"_RenderLayers.nk"
    nuke.scriptSaveAndClear(pre_comp)

    #open child shot
    nuke.scriptOpen(comp_path)

    #import child playblast
    
    readNode = nuke.nodes.Read()
    readNode.knob('file').fromUserText(child)
    readNode.knob("tile_color").setValue(int("FFFF00FF", 16))
    readNode.knob("label").setValue("[value first] - [value last]")
    oPath =  os.path.basename(nuke.root().name())
    file = os.path.basename(oPath).split("_")
    project = os.path.basename(oPath).split("_")[0]
    ep = os.path.basename(oPath).split("_")[1]
    seq = os.path.basename(oPath).split("_")[2]
    shot = os.path.basename(oPath).split("_")[3]
    dir = os.path.dirname(oPath)

    #if (project == 'puf'):
    #    new_path = ("P:/01prj/PUF/prod/approved/"+ep+"/Animation/Approved/")
    #elif (project == 'aaj'):
    #    new_path = ("A:/01prj/AAJ/prod/approved/"+ep+"/Animation/Approved/")

    new_file_name = (project+"_"+ep+"_"+seq+"_"+shot+"_")
    #for file in os.listdir(new_path):

        #if file.startswith(new_file_name):
              #print(file)
              #print(os.path.join(new_path, file))
              #new_anim_path = os.path.join(new_path, file)
              #readNode = nuke.nodes.Read()
              #readNode.knob('file').fromUserText(new_anim_path)
              #readNode.knob("tile_color").setValue(int("FFFF00FF", 16))
              #readNode.knob("label").setValue("[value first] - [value last]")
              #break
    #take playblast frame range
    first_frame = str(int(readNode['first'].value())+100)
    last_frame = str(int(readNode['last'].value())+100)
    #update project setting
    nuke.knob("root.first_frame",first_frame)
    nuke.knob("root.last_frame",last_frame)
    nuke.knob("root.fps","25")
    nuke.knob("root.format","HD_1080")
    #update read node
    n = nuke.allNodes()
    for i in n:
        if i.Class() == "Read":
            if i["file"].value().lower().endswith(".exr"):
                Path =  i["file"].value()
                try:
                    Path = re.sub(parent_project, child_project, Path)
                    Path = re.sub(parent_ep, child_ep, Path)
                    Path = re.sub(parent_seq, child_seq, Path)
                    Path = re.sub(parent_shot, child_shot, Path)
                    Path = re.sub(parent_shot, child_shot, Path)
                    dir = os.path.dirname(Path)
                except:
                    dir = os.path.dirname(Path)
                print(dir)
                if os.path.exists(dir):
                    for render_file in nuke.getFileNameList(dir):
                        print(render_file)
                        i.knob('file').fromUserText(dir +'/'+ render_file)

                #i['file'].fromUserText(new_path)
    nuke.scriptSave(comp_path)

            #print(Path)



    nuke.message (nuke_file+" created by "+username+".\nBefore you proceed, check the render layers and copy the write node.")
    nuke.scriptOpen(pre_comp)
