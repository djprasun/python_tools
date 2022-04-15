import streamlit as st
from streamlit import caching
import os
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pyautogui
import shutil 


st.set_page_config(layout="wide")


time_slot = st.empty()





auto = st.sidebar.checkbox('Auto refresh',help='Only use during standby')




#input_sec = st.sidebar.number_input('Refresh rate/sec', min_value=10)

#my_slot3 = st.sidebar.empty()
my_slot = st.sidebar.empty()
my_slot2 = st.sidebar.empty()
    
    
st.title("Compositing: Shot Summary")



@st.cache(allow_output_mutation=True)

#@st.cache(allow_output_mutation=True)
def load_data():
  
    
    
        
    try:
        
        df = pd.DataFrame(pd.read_csv("D:\prasun\TEST EXCEL\AAJ_POST_STATUS.csv"))
        
        return df
        
    except:
        
    
        
        
        caching.clear_cache()
        st.experimental_rerun()
        
    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh

# Will only run once if already cached
df = load_data()
df = df[df['EP'].notna()]
#convert data
df['shot_index'] = df['EP']+'_'+df['SEQ']+'_'+df['SHOT']
df.set_index('shot_index', inplace = True)
df['FRAMES'].fillna(0)

convert_frame = pd.Series(df["FRAMES"])
pd.to_numeric(convert_frame)
df["FRAMES"] = df["FRAMES"].apply(pd.to_numeric)



st.subheader('Last updated: '+time.ctime())
last_update = time.ctime()

st.write('Total rows: '+ str(len(df)))


    





#---sidebar
st.sidebar.header('User Input')

#---select episode
#df.final.fillna('NO ENTRY')
sorted_episode = list(df['EP'].fillna('NO ENTRY').unique())
episode_container = st.sidebar.beta_container()
all_episode = st.sidebar.checkbox("Select all episodes")
if all_episode:
    episode_select = episode_container.multiselect("Select one or more episodes:",
         sorted_episode,sorted_episode)
else:
    episode_select =  episode_container.multiselect("Select one or more episodes:",
        sorted_episode,['EP627','EP530'])


list_of_ep = ' + '.join(map(str,episode_select))

st.write('You selected:', list_of_ep)  
     
 #---select artist        
filt_ep_artist = df[(df.EP.isin(episode_select))]


sorted_artist = list(filt_ep_artist['COMP_ARTIST'].unique())

artist_container = st.sidebar.beta_container()
all_artist = st.sidebar.checkbox("Select all comp artists", True)
 
if all_artist:
    selected_artist = artist_container.multiselect("Select one or more comp artists:",
         sorted_artist,sorted_artist)
else:
    selected_artist =  artist_container.multiselect("Select one or more comp artists:",
        sorted_artist)

#---main filter

df.filt_ep = df[(df.EP.isin(episode_select)) & (df.COMP_ARTIST.isin(selected_artist))]

#----all shots
st.write('Total shots:', len(df.filt_ep['EP']))
all_shots = ('All shots: '+ str(len(df.filt_ep['EP'])))
#--- not moved to comp
df.not_moved = df.filt_ep[(df.filt_ep.LIT_STATUS != 'READY FOR COMP')] 
not_moved = ( 'Shots not moved to comp: '+str(len(df.not_moved['EP'])))

#----unassigned_shots
    
df.filt_not_assigned = df.filt_ep[(df.filt_ep['LIT_STATUS'] == 'READY FOR COMP') & (df.filt_ep['COMP_ARTIST'].isna())]
unassigned_shots = ('Unassigned shots: '+str(len(df.filt_not_assigned['COMP_ARTIST'])))
    

    
#filter master
df.filt_master = df.filt_ep[(df.filt_ep['Type'] == 'MASTER')]
master_shots = ( 'Master shots: '+str(len(df.filt_master['EP'])))
#st.write('Total mastershots in this episode:', len(df.filt_master['EP']))
#master_shots = st.checkbox('Show master shots')
#if master_shots:
    
#    st.write(df.filt_master[['FRAMES','COMP_ARTIST','COMP_STATUS']])
    
    
#---3dc shots
df.threedc = df.filt_ep[(df.filt_ep.COMP_STATUS == 'LIT 3DC') 
                       |(df.filt_ep.COMP_STATUS == 'LIT 3DC RENDER')
                       |(df.filt_ep.COMP_STATUS == 'LIT 3DC RENDER DONE')
                       |(df.filt_ep.COMP_STATUS == 'FX 3DC')] 
                      
                      #& (df.filt_ep['COMP_STATUS'] == 'FX 3DC')]
                    
threedc =   ('3DC shots: '+str(len(df.threedc['EP'])))      



                   
#--- filter on floor

df.filt_assigned_shots = df.filt_ep.dropna(subset=['COMP_ARTIST'])
df.filt_on_floor = df.filt_assigned_shots[(df.filt_assigned_shots['COMP_STATUS'] != 'LIT 3DC')
                                        & (df.filt_assigned_shots['COMP_STATUS'] != 'LIT 3DC RENDER')
                                        & (df.filt_assigned_shots['COMP_STATUS'] != 'FX 3DC')
                                        & (df.filt_assigned_shots['COMP_STATUS'] != 'TO CHECK')
                                        & (df.filt_assigned_shots['FINAL_STATUS'] != 'DONE')]
 

on_floor = ('Shots on floor: '+str(len(df.filt_on_floor['EP'])))

#--pending review

df.filt_pending_review = df.filt_ep[(df.filt_ep['COMP_STATUS'] == 'TO CHECK') & (df.filt_ep['FINAL_STATUS'] != 'DONE') ]
pending_review = ('Shots pending review: '+str(len(df.filt_pending_review['EP'])))

#---not done
df.not_done = df.filt_ep[(df.filt_ep['FINAL_STATUS'] != 'DONE')]
not_done = ('Shots not done: '+str(len(df.not_done['EP'])))



 #---adding first column
acol1,acol2= st.beta_columns([1,3])
 
#df.final = df.filt_ep

with acol1:
    if st.button ('Reload database'):
        caching.clear_cache()
        load_data()
        
        pyautogui.hotkey('f5') #Simulates F5 key press = page refresh
        
        #st.experimental_rerun()
     
  
 
        
    
    
    status_selection = st.radio("Select status:", (all_shots, not_moved , unassigned_shots , master_shots , threedc ,on_floor,pending_review,not_done))
    
    
    #adding buttons
    report_selection = st.radio("Select report type:", ('Text', 'Pie (Episode)' ,'Table' , 'Bubble chart' , 'Pie (Artist)' , 'Bar (Artist)'))
    
    colour_slot = st.empty()
    

    
    
with acol2:
    if status_selection == all_shots:
        st.subheader('All shot')
        df.final = df.filt_ep
    
    if status_selection == not_moved:
        st.subheader('Shots that are not moved to comp')
        df.final = df.not_moved

    if status_selection == unassigned_shots:
        st.subheader('Unassigned shots')
        df.final = df.filt_not_assigned
    
    if status_selection == master_shots:
        st.subheader('Master shot')
        df.final = df.filt_master
    
    if status_selection == threedc:
        st.subheader('3DC shot')
        df.final = df.threedc
    if status_selection == on_floor:
        st.subheader('On floor shot')
        st.markdown(' ')
        df.final = df.filt_on_floor
    if status_selection == pending_review:
        st.subheader('Pending review shot')
        df.final = df.filt_pending_review
    if status_selection == not_done:
        st.subheader('Not done shots')
        df.final = df.not_done




    if report_selection == 'Text':
        #st.subheader('Showing texts')
        st.write('Total: '+str(len(df.final['EP'])))
        df.text_episode_unique = df.final['EP'].unique()
        df.text_episode_value = df.final['EP'].value_counts().add_suffix(' = ')
        
        for col_name, data in df.text_episode_value.items():
            st.write(col_name,str(data))
        
        df.text_artist_unique = df.final['COMP_ARTIST'].unique()
        df.text_artist_value = df.final['COMP_ARTIST'].value_counts().add_suffix(' = ')
        
        st.subheader('Artist')
        for col_name, data in df.text_artist_value.items():
            st.write(col_name,str(data))
            
        df.moved = df.final[(df.final.LIT_STATUS == 'READY FOR COMP')]
        text = ('Ready for comp: '+str(len(df.moved['EP'])))
        st.subheader(text)
 
        df.done = df.final[(df.final.FINAL_STATUS == 'DONE')] 
        text = ('Done: '+str(len(df.done['EP'])))
        st.subheader(text) 
        
        df.correction = df.final[(df.final.COMP_STATUS == 'LIT 3DC') 
                       |(df.final.COMP_STATUS == 'LIT 3DC RENDER')
                       |(df.final.COMP_STATUS == 'LIT 3DC RENDER DONE')
                       |(df.final.COMP_STATUS == 'FX 3DC')] 
        text = ('3DC: '+str(len(df.correction['EP'])))
        st.subheader(text) 
        
        df.onfloor = df.final[(df.final['COMP_STATUS'] != 'LIT 3DC')
                                        & (df.final['COMP_STATUS'] != 'LIT 3DC RENDER')
                                        & (df.final['COMP_STATUS'] != 'FX 3DC')
                                        & (df.final['COMP_STATUS'] != 'TO CHECK')
                                        & (df.final['FINAL_STATUS'] != 'DONE')]
        text = ('Shots on floor: '+str(len(df.correction['EP'])))                               
        
        df.notdone = df.final[(df.final.FINAL_STATUS != 'DONE')]
        text = ('Yet to complete: '+str(len(df.notdone['EP'])))
        st.subheader(text) 
        
        #df.filt_assigned_shots = df.final.dropna(subset=['COMP_ARTIST'])
        df.filt_on_floor = df.final[(df.final['COMP_STATUS'] != 'LIT 3DC')
                                        & (df.final['COMP_STATUS'] != 'LIT 3DC RENDER')
                                        & (df.final['COMP_STATUS'] != 'LIT 3DC RENDER DONE')
                                        & (df.final['COMP_STATUS'] != 'FX 3DC')
                                        & (df.final['COMP_STATUS'] != 'TO CHECK')
                                        & (df.final['FINAL_STATUS'] != 'DONE')]
        text = ('On floor: '+str(len(df.filt_on_floor['EP'])))
        st.subheader(text)
        
        
        
    if report_selection == 'Bubble chart':
        st.subheader('Showing bubble charts')
        st.write(px.scatter(df.final.fillna('NO ENTRY'), x='COMP_STATUS', y='FRAMES', color='COMP_ARTIST', 
             facet_col='EP', facet_row='FINAL_STATUS', size='FRAMES', hover_data = [df.final.index],height=700,width=1200, color_discrete_map={'NO ENTRY': 'black'},
             category_orders={'EP': ['EP'],'FINAL_STATUS': ['FINAL_STATUS']}))  
    
    if report_selection == 'Table':
        st.subheader('Showing tables')
        
        df['EP'] = df['EP'].fillna('NO ENTRY')
        st.write(df.final['EP'].value_counts())
        
        df.final['LIT_STATUS'] = df.final['LIT_STATUS'].fillna('NO ENTRY')
        st.write(df.final['LIT_STATUS'].value_counts())
        
        df.final['COMP_STATUS'] = df.final['COMP_STATUS'].fillna('NO ENTRY')
        st.write(df.final['COMP_STATUS'].value_counts())
        
        df.final['FINAL_STATUS'] = df.final['FINAL_STATUS'].fillna('NO ENTRY')
        st.write(df.final['FINAL_STATUS'].value_counts())
        
        df.final['COMP_ARTIST'] = df.final['COMP_ARTIST'].fillna('NO ENTRY')
        df.ch_frame = (df.final.groupby('COMP_ARTIST')['Sec','FRAMES'].sum())
        df.ch_count = (df.final['COMP_ARTIST'].value_counts())
        df.ch_flt = pd.concat([df.ch_count, df.ch_frame], axis=1, join="inner") 
        
        st.write(df.ch_flt)
        
    if report_selection == 'Pie (Artist)':
        st.subheader('Showing Pie (Artist)')
        st.write(px.sunburst(df.final.fillna('NO ENTRY'), path=['COMP_ARTIST','COMP_STATUS','FINAL_STATUS',df.final.index], values= 'FRAMES', color='FINAL_STATUS',width=1000, height=600, hover_data = df.final.value_counts()))
      
    if report_selection == 'Pie (Episode)':
        st.subheader('Showing Pie (Episode)')
        path_selection_list = ['EP','LIT_STATUS', 'COMP_STATUS','FINAL_STATUS','COMP_ARTIST','SHOT_INDEX']
        path_selection = path_selection_list
        pie_color = colour_slot.selectbox('Colour', path_selection_list)
        if pie_color == 'SHOT_INDEX':
            path_selection_list = ['EP','LIT_STATUS', 'COMP_STATUS','FINAL_STATUS','COMP_ARTIST',df.final.index]
            pie_color = df.final.index
        st.write(px.sunburst(df.final.fillna('NO ENTRY'), path=['EP','LIT_STATUS', 'COMP_STATUS','FINAL_STATUS','COMP_ARTIST',df.final.index], values= 'FRAMES', color = pie_color, width=1000, height=600))
        st.write(px.bar(df.final, x='FRAMES', y='COMP_ARTIST', hover_data = [df.final.index],width=900, color='EP'))  
     
        
    #st.write(px.bar(df.final, x='Sec', y='COMP_ARTIST', color='EP'))
    #st.write(px.pie(df.final, values=('Sec'), names='COMP_ARTIST'))
    
    
    
             
    
 #---adding second column
a1col1,a2col2= st.beta_columns([1,1])   
    

    

    
  
    #st.bar_chart(df.final['EP'].value_counts())
    #st.bar_chart(df.final['LIT_STATUS'].value_counts())
    #st.bar_chart(df.final['COMP_STATUS'].value_counts())
    #st.bar_chart(df.final['FINAL_STATUS'].value_counts())
    #st.write(px.bar(df.final, x='Sec', y='COMP_ARTIST', color='EP'))


           
#---operation of the button  
#df.final = df.filt_ep         


    
    
#---adding second column
            
bcol1,bcol2,bcol3,bcol4,bcol5 = st.beta_columns([.5,1,1,.8,1.5])


with bcol1:
    
    st.bar_chart(df.final['EP'].value_counts())
    df.tab = (df.final['EP'].value_counts())
    #st.dataframe(tabulate(df.tab, headers = 'keys', tablefmt = 'psql'))
    
            
            

with bcol2:
    
    st.bar_chart(df.final['LIT_STATUS'].value_counts())
    
with bcol3:   
    
    st.bar_chart(df.final['COMP_STATUS'].value_counts())
    
with bcol4:
    
    st.bar_chart(df.final['FINAL_STATUS'].value_counts())
    
with bcol5:   
    
    
    #fig = px.scatter(df.ch_flt,x='COMP_ARTIST', y='FRAMES', color=df.final['COMP_ARTIST'].value_counts(), size = 'FRAMES', hover_data=['COMP_ARTIST'])
    #st.write(fig)
    
    #st.bar_chart(df.ch_flt)
        
    st.write(px.bar(df.final, x='Sec', y='COMP_ARTIST', color='EP'))
    st.write(px.pie(df.final, values=('Sec'), names='COMP_ARTIST'))
    
    
    

        
        



st.write(df.final[['FRAMES','LIT_STATUS','COMP_ARTIST','COMP_STATUS','FINAL_STATUS','COMP_INT_CORR']])
#for index, row in df.final.iterrows():
#    st.checkbox (index+' '+ str(row['COMP_INT_CORR']))       
#time.sleep(30)

input_sec = 10
if auto:
    
    #for _ in stqdm(range(50), desc="This is a slow task", mininterval=1):
    #my_slot2 =  my_bar   #sleep(0.5)
    
    my_bar = my_slot2.progress(0)
    
    progres_divide = input_sec/100
    
    
    def countdown(time_sec,divide):
            
            while time_sec:
                
                mins, secs = divmod(time_sec, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                my_slot.write('Refresh in: '+timeformat, end='\r')
                time.sleep(1)
                time_sec -= 1
                my_bar.progress(time_sec*divide)
                

            my_slot.write("Refreshing...")
            source1 = r"A:\01prj\AAJ\prod\shotpub\Allotment\Post_Final_Status\AAJ_POST_STATUS.xls"
         
            destination1 = r"D:\prasun\TEST EXCEL\AAJ_POST_STATUS.xls"
            shutil.copy(source1, destination1)

               
    countdown(input_sec,progres_divide)
    caching.clear_cache()
    st.experimental_rerun()
    
    
    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh

#st.stop()
