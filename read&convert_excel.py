import pandas as pd
import os
import time
import shutil
from alive_progress import alive_bar
from progress.spinner import MoonSpinner
from progress.bar import Bar
from time import sleep
#from tqdm.notebook import tqdm_notebook
#tqdm_notebook.pandas()
import time
import progressbar
import io
import os, sys
from datetime import date
import calendar




#selected_episode = ['EP325','EP426','EP525','EP530','EP725','EP825','EP727']
selected_episode = ['EP831','EP730','EP829','EP626']
#selected_episode = ['EP325','EP426','EP525']

def copy():
    
    today = date.today()
    
    day_of_week = today.weekday()+1
    days_elapsed = day_of_week 
    deadline = 6
    days_left = deadline - day_of_week
    no_of_artist = 4
    
    day = calendar.day_name[today.weekday()]
    
    begin = time.time()
    

    # Source path
    source1 = r"P:\01prj\PUF\prod\shotpub\Allotment\Post_Final_Status\AAJ_POST_STATUS_V02.xls"
    # Destination path
    destination1 = r"D:\prasun\TEST EXCEL\AAJ_POST_STATUS.xls"
    shutil.copy(source1, destination1)
    
    

        
    read_file1 = pd.read_excel (r"D:\prasun\TEST EXCEL\AAJ_POST_STATUS.xls", 'Sheet1')
    read_file1.to_csv ("D:\prasun\TEST EXCEL\AAJ_POST_STATUS.csv", index = None, header=True)
    

    #BACKUP IN SERVER
    source1 = r"D:\prasun\TEST EXCEL\AAJ_POST_STATUS.csv"
    destination1 = r"P:\01prj\PUF\prod\shotpub\Allotment\Artist_Backup\Prasun\very imp_dont delete\excel_conversion\AAJ_POST_STATUS.csv"
    shutil.copy(source1, destination1)
    
    
    aaj_df = pd.DataFrame(pd.read_csv(r"D:\prasun\TEST EXCEL\AAJ_POST_STATUS.csv"))
    
        #bar()
    
    divider = '##################################################################################'


    
    sorted_episode = list(aaj_df['Episode'].fillna('NO ENTRY').unique())
    #selected_episode = sorted_episode
    aaj_df['Episode'] = aaj_df['Episode'].str.upper()
    aaj_df['COMP_ARTIST'] = aaj_df['COMP_ARTIST'].str.upper()
    
    os.system('cls')
    
    for ep in selected_episode:
        print(ep)
       
        sel_df = aaj_df[(aaj_df['Episode'].isin([ep]))]
        
        #TOTAL
        total = ('TOTAL: '+str(len(sel_df)))
        #total = ('TOTAL: '+str(len(sel_df)))
        #print(total)
        aaj_text_artist_value = sel_df['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = total
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        
        #NOT READY
        not_yet_ready = sel_df[(sel_df ['LIT_STATUS'] != 'READY FOR COMP')]
        aaj_not_yet_ready_ep_value = not_yet_ready['Episode'].value_counts().add_suffix('-')
        print('NOT READY FOR COMP: ' + str(len(not_yet_ready)))
        
        #DONE
        filt_done = sel_df[(sel_df['FINAL_STATUS'] == 'DONE')]
        done = ('DONE: '+str(len(filt_done)))
        #print (done)
        aaj_text_artist_value = filt_done['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = done
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        
        #NOT DONE
        filt_not_done = sel_df[(sel_df ['FINAL_STATUS'] != 'DONE')]
        not_done = ('NOT DONE: '+str(len(filt_not_done)))
        #print (not_done)
        aaj_text_artist_value = filt_not_done['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = not_done
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        
        #3DC
        threedc = sel_df[(sel_df.COMP_STATUS == 'LIT 3DC') 
                       |(sel_df.COMP_STATUS == 'LIT 3DC RENDER')
                       |(sel_df.COMP_STATUS == 'LIT 3DC RENDER DONE')
                       |(sel_df.COMP_STATUS == 'FX 3DC')]   
        aaj_text_artist_value = threedc['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = ('3DC SHOT: '+str(len(threedc['Episode'])))
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)


        #TO CHECK
        pendingdf = sel_df.loc[(sel_df.COMP_STATUS == "TO CHECK") & (sel_df.FINAL_STATUS != "DONE")]
        pending_review = ('TO CHECK: '+str(len(pendingdf)))  
        aaj_text_artist_value = pendingdf['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = pending_review
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)    
        
        #ON FLOOR
        aaj_filt_on_floor = sel_df[(sel_df ['LIT_STATUS'] == 'READY FOR COMP')
                                            &  (sel_df['COMP_STATUS'] != 'LIT 3DC')
                                            & (sel_df['COMP_STATUS'] != 'LIT 3DC RENDER')
                                            & (sel_df['COMP_STATUS'] != 'LIT 3DC RENDER DONE')
                                            & (sel_df['COMP_STATUS'] != 'FX 3DC')
                                            & (sel_df['COMP_STATUS'] != 'TO CHECK')
                                            & (sel_df['FINAL_STATUS'] != 'DONE')]
        on_floor = ('ON FLOOR: '+str(len(aaj_filt_on_floor)))
        aaj_text_artist_value = aaj_filt_on_floor['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = on_floor
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
                       
        #ATTEMPTED
        aaj_filt_attempted = sel_df[(sel_df ['LIT_STATUS'] == 'READY FOR COMP')
                                            &  (sel_df.COMP_STATUS.notnull())]
        attempted = ('ATTMPTED: '+str(len(aaj_filt_attempted)))
        aaj_text_artist_value = aaj_filt_attempted['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = attempted
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        
        # REVIEWD
        aaj_reviewed = sel_df[(sel_df ['LIT_STATUS'] == 'READY FOR COMP' ) &  (sel_df.FINAL_STATUS.notnull())]
        rev = ('REVIEWED: '+str(len(aaj_reviewed)))
        aaj_text_artist_value = aaj_reviewed['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = rev
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        

        
        # NOT REVIEWD
        aaj_not_reviewed = sel_df[(sel_df ['LIT_STATUS'] == 'READY FOR COMP' )& (sel_df['FINAL_STATUS'] != 'INT CORR') & (sel_df['FINAL_STATUS'] != 'DONE')]
        not_rev = ('NOT REVIEWED: '+str(len(aaj_not_reviewed)))
        aaj_text_artist_value = aaj_not_reviewed['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = not_rev
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        
        #INTERNAL CORRECTION
        aaj_int_cor = sel_df[(sel_df ['LIT_STATUS'] == 'READY FOR COMP' )& (sel_df['FINAL_STATUS'] == 'INT CORR')]
        int_cor = ('INTERNAL CORRECTION: '+str(len(aaj_int_cor)))
        aaj_text_artist_value = aaj_int_cor['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = int_cor
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        
        
        
        #UNTOUCHED
        aaj_filt_untouched = sel_df[(sel_df ['LIT_STATUS'] == 'READY FOR COMP')
                                            &  (sel_df.COMP_STATUS.isnull())]
        untouched = ('UNTOUCHED: '+str(len(aaj_filt_untouched)))
        aaj_text_artist_value = aaj_filt_untouched['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
        one_line = untouched
        for col_name, data in aaj_text_artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        
        print(divider)  

        
    aaj_df = aaj_df[(aaj_df['Episode'].isin(selected_episode))]
    pendingdf = aaj_df.loc[(aaj_df.COMP_STATUS == "TO CHECK") & (aaj_df.FINAL_STATUS != "DONE")]

    pending_review = ('TO CHECK: '+str(len(pendingdf)))
    

    aaj_filt_on_floor = aaj_df[(aaj_df ['LIT_STATUS'] == 'READY FOR COMP')
                                            &  (aaj_df['COMP_STATUS'] != 'LIT 3DC')
                                            & (aaj_df['COMP_STATUS'] != 'LIT 3DC RENDER')
                                            & (aaj_df['COMP_STATUS'] != 'LIT 3DC RENDER DONE')
                                            & (aaj_df['COMP_STATUS'] != 'FX 3DC')
                                            & (aaj_df['COMP_STATUS'] != 'TO CHECK')
                                            & (aaj_df['FINAL_STATUS'] != 'DONE')]
                                            
    total_on_floor = len(aaj_filt_on_floor)
    

    on_floor = ('ON FLOOR: '+str(total_on_floor))
    not_yet_ready = aaj_df[(aaj_df['Episode'] .isin(selected_episode)) & (aaj_df ['LIT_STATUS'] != 'READY FOR COMP')]
    
    grand_total = str(len(aaj_df['Episode'] .isin(selected_episode)))
    grand_total_avg = int(int(grand_total)/deadline)
    total = ('GRAND TOTAL: '+ grand_total)
    threedc = aaj_df[(aaj_df.COMP_STATUS == 'LIT 3DC') 
                       |(aaj_df.COMP_STATUS == 'LIT 3DC RENDER')
                       |(aaj_df.COMP_STATUS == 'LIT 3DC RENDER DONE')
                       |(aaj_df.COMP_STATUS == 'FX 3DC')] 
                      
                      
                    
     
                                            
                                          
                                            
    filt_done = aaj_df[(aaj_df['FINAL_STATUS'] == 'DONE')]
    total_done = len(filt_done)
    total_done_avg = int(total_done/day_of_week)
    done = ('DONE: '+str(total_done))
    
    
    filt_not_done = aaj_df[(aaj_df['Episode'] .isin(selected_episode)) & (aaj_df ['FINAL_STATUS'] != 'DONE')]
    total_not_done = len(filt_not_done)
    
    not_done = ('NOT DONE: '+str(total_not_done))
    
    
    

    #print ('Episode: ' + selected_episode)
    list_of_ep = ' & '.join(map(str,selected_episode))

  
    
    
        
    aaj_total_ep_value = aaj_df['Episode'].value_counts().add_suffix('-')

    one_line = " "
    for col_name, data in aaj_total_ep_value.items():
        
        #print('-'+col_name,str(data))
        
        one_line = one_line+' | '+col_name+str(data)
   
    print(total+one_line)
    aaj_text_artist_value = aaj_df['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)
    
    #print(aaj_df)
    
    
    aaj_done_ep_value = filt_done['Episode'].value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_done_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
        
    print(done+one_line)
    aaj_text_artist_value = filt_done['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)
    
    aaj_not_done_ep_value = filt_not_done['Episode'].value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_not_done_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
        
    print(not_done+one_line)    
    aaj_text_artist_value = filt_not_done['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)    
    

    
    
    aaj_not_yet_ready_ep_value = not_yet_ready['Episode'].value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_not_yet_ready_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
        
    print('NOT READY FOR COMP: ' + str(len(not_yet_ready))+one_line)    
        
        
    #print (threedc)
    
    aaj_threedc_ep_value = threedc['Episode'].value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_threedc_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print('3DC SHOT: '+str(len(threedc['Episode']))+one_line)    
    aaj_text_artist_value = threedc['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)    
        
    
    aaj_pending_review_ep_value = pendingdf['Episode'].value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_pending_review_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(pending_review+one_line)    
    aaj_text_artist_value = pendingdf['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)    
    
    aaj_on_floor_ep_value =  aaj_filt_on_floor['Episode'].value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_on_floor_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(on_floor+one_line)    
    #aaj_text_artist_unique = aaj_filt_on_floor['COMP_ARTIST'].unique()
    aaj_text_artist_value = aaj_filt_on_floor['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)
    
    #ATTEMPTED
    aaj_filt_attempted = aaj_df[(aaj_df ['LIT_STATUS'] == 'READY FOR COMP')
                                        &  (aaj_df.COMP_STATUS.notnull())]
    total_attempted = len(aaj_filt_attempted)
    total_attempted_avg = int(total_attempted/days_elapsed)
    aaj_filt_attempted_ep_value = aaj_filt_attempted['Episode'].value_counts().add_suffix('-')                                    
    attempted = ('ATTMPTED: '+str(total_attempted))
    one_line = " "
    for col_name, data in aaj_filt_attempted_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(attempted+one_line)
    
    aaj_text_artist_value = aaj_filt_attempted['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)
    
        #REVIEWED
    aaj_reviewed = aaj_df[(aaj_df ['LIT_STATUS'] == 'READY FOR COMP' ) &  (aaj_df.FINAL_STATUS.notnull())]
    total_reviewed = len(aaj_reviewed)
    total_reviewed_avg = int(total_reviewed/days_elapsed)
    aaj_reviewed_ep_value = aaj_reviewed['Episode'].value_counts().add_suffix('-')
    rev = ('REVIEWED: '+str(total_reviewed))
    one_line = " "
    for col_name, data in aaj_reviewed_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(rev+one_line)
    
    aaj_text_artist_value = aaj_reviewed['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)
    
    # NOT REVIEWD
    aaj_not_reviewed = aaj_df[(aaj_df ['LIT_STATUS'] == 'READY FOR COMP' )& (aaj_df['FINAL_STATUS'] != 'INT CORR') & (aaj_df['FINAL_STATUS'] != 'DONE')]
    total_not_reviewed = len(aaj_not_reviewed)
    
    aaj_not_reviewed_ep_value = aaj_not_reviewed['Episode'].value_counts().add_suffix('-')
    not_rev = ('NOT REVIEWED: '+str(total_not_reviewed))
    one_line = " "
    for col_name, data in aaj_not_reviewed_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(not_rev+one_line)
    
    aaj_text_artist_value = aaj_not_reviewed['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)
    
        
    

    
    
    #INTERNAL CORRECTION
    aaj_int_cor = aaj_df[(aaj_df ['LIT_STATUS'] == 'READY FOR COMP' )& (aaj_df['FINAL_STATUS'] == 'INT CORR')]
    aaj_int_cor_ep_value = aaj_int_cor['Episode'].value_counts().add_suffix('-')
    int_cor = ('INTERNAL CORRECTION: '+str(len(aaj_int_cor)))
    one_line = " "
    for col_name, data in aaj_int_cor_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(int_cor+one_line)
    
    aaj_text_artist_value = aaj_int_cor['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)
    
    #UNTOUCHED
    aaj_filt_untouched = aaj_df[(aaj_df ['LIT_STATUS'] == 'READY FOR COMP')
                                        &  (aaj_df.COMP_STATUS.isnull())]
    total_untouched = len(aaj_filt_untouched)
    
    aaj_filt_untouched_ep_value = aaj_filt_untouched['Episode'].value_counts().add_suffix('-')                                    
    untouched = ('UNTOUCHED: '+str(total_untouched))
    one_line = " "
    for col_name, data in aaj_filt_untouched_ep_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(untouched+one_line)
    
    aaj_text_artist_value = aaj_filt_untouched['COMP_ARTIST'].fillna('Not assigned').value_counts().add_suffix('-')
    one_line = " "
    for col_name, data in aaj_text_artist_value.items():
        one_line = one_line+' | '+col_name+str(data)
    print(one_line)
    
    
    
    
def retry():
    #os.system('cls')
    print("Error occurred...retrying")
    with alive_bar(30, bar = 'circles') as bar:
            for i in range(30):
                sleep(1.00)
                bar()
    while True:
        try:
            copy()
            hour()
            with alive_bar(10, bar = 'circles') as bar:
                for i in range(10):
                    sleep(1.00)
                    bar() 
        except:
            retry()
            with alive_bar(10, bar = 'circles') as bar:
                for i in range(10):
                    sleep(1.00)
                    bar()

# BACKUP                    
def hour():
    import time
    import shutil
    time = time.ctime()
    day = time[:3]
    hr = time[11:13]
    min = time[14:16]
    hr_name = (day+"_"+hr+"_hrs")

    #print(file_name)
    source1 = r"D:\prasun\TEST EXCEL\AAJ_POST_STATUS.csv"
    destination1 = r"D:\prasun\TEST EXCEL\date\\"+hr_name+".csv"
    shutil.copy(source1, destination1)
    
    min_name = (hr+"_"+min)
    #print(file_name)
    source1 = r"D:\prasun\TEST EXCEL\AAJ_POST_STATUS.csv"
    destination1 = r"D:\prasun\TEST EXCEL\date\day\\"+min_name+".csv"
    shutil.copy(source1, destination1)



           
                    
def true():
    while True:
        
        try:
            copy()
            hour()
           
            with alive_bar(10, bar = 'circles') as bar:
                    for i in range(10):
                        sleep(1.00)
                        bar() 
        except:
            
            retry()
copy()
hour()
true()

      