import shutil
import pandas as pd
from alive_progress import alive_bar
from progress.spinner import MoonSpinner
from progress.bar import Bar    
from time import sleep
import time
import ctypes
import os, sys    
def copy():    
    # Source path
    log = r"P:/01prj/PUF/prod/shotpub/Allotment/Artist_Backup/Prasun/very imp_dont delete/"
    excel_file = "logs/artist_log.csv"
    log_file = log + excel_file
    #print(log_file)
    try:
        
        # Destination path
        log_file_copy = log+"for_everyone\\artist_log.csv"
        
        shutil.copy(log_file, log_file_copy)
    except:
        log_file_copy = log+"for_everyone\\backup\\artist_log.csv"
        
        shutil.copy(log_file, log_file_copy)
        
    df = pd.DataFrame(pd.read_csv(log_file_copy))
    os.system('cls')
    
    
    import time
    import datetime
    time = time.ctime()
    
    print("Time: "+time)
    print("Last 7 days")
    
    
    
    time_list = df ['DATE'].str[:10].unique().tolist()
    
    for time in time_list[-7:]:
        
        
        
        
        sel_df = df[(df['DATE'].str[:10].isin([time]))]
        
        filt_attempted = sel_df[(sel_df ['DATE'].str[:10] == time)]
        artist_value = filt_attempted['USER'].value_counts().add_suffix('-')
        one_line = (time+': '+str(len(filt_attempted['USER'])))
        for col_name, data in artist_value.items():
            one_line = one_line+' | '+col_name+str(data)
        print(one_line)
        
    print(('*')*100)
    print("Last 25 entries")
    print(df.iloc[-25:])
    
    
    
    
    
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
def true():
    while True:
        try:
            copy()
            with alive_bar(10, bar = 'circles') as bar:
                    for i in range(10):
                        sleep(1.00)
                        bar() 
        except:
            retry()
copy()
true()