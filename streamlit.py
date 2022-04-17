import streamlit as st

import pandas as pd
import time
#import pyautogui
import plotly.express as px


st.set_page_config(layout="wide",initial_sidebar_state="collapsed")









#st.title("Compositing: Shot Summary")


@st.cache(allow_output_mutation=True)

#@st.cache(allow_output_mutation=True)
def load_data():




    try:

        df = pd.DataFrame(pd.read_csv("D:\prasun\TEST EXCEL\AAJ_POST_STATUS.csv"))

        return df

    except:




        st.legacy_caching.clear_cache()
        st.experimental_rerun()

    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh

# Will only run once if already cached
df = load_data()
#fill up blank columns
df = df[df['Episode'].notna()]
df['FRAMES'].fillna(0)
df['COMP_STATUS'].fillna(0)
df['Episode'] = df['Episode'].str.upper()
#create new column for the shot name to create new index
df['shot_index'] = df['Episode']+'_'+df['SEQ']+'_'+df['SHOT']

df.set_index('shot_index', inplace = True)
df['shot_index'] = df['Episode']+'_'+df['SEQ']+'_'+df['SHOT']

convert_frame = pd.Series(df["FRAMES"])
pd.to_numeric(convert_frame)
df["FRAMES"] = df["FRAMES"].apply(pd.to_numeric)
#st.sidebar.subheader(time.ctime())

# setup auto refresh

auto = st.sidebar.checkbox('Auto reload',help='Only use during standby')
my_slot = st.sidebar.empty()
my_slot2 = st.sidebar.empty()
reload_button = my_slot.button('Reload database')
if reload_button:
        st.legacy_caching.clear_cache()
        #st.experimental_rerun()
        load_data()
        st.legacy_caching.clear_cache()
        st.legacy_caching.clear_cache()
        #st.experimental_rerun()
        #pyautogui.hotkey('f5')




#---sidebar
st.sidebar.header('Filters')
path_selection_list = ['Episode','FINAL_STATUS','COMP_STATUS','COMP_ARTIST','LIT_STATUS','SHOT_INDEX']
path_selection = path_selection_list
color = st.sidebar.selectbox('Bar colour', path_selection_list)

status_selection = st.sidebar.selectbox('Select status', ['All Shots','Not ready of comp','Done','Not Done','3DC','To Check','On Floor','Attempted','Reviewed','Not reviewed','Internal Correction','Untouched','Not assigned'])


#populate sidebar

#---select episode

sorted_episode = list(df['Episode'].fillna('NO ENTRY').unique())
episode_container = st.sidebar.container()
all_episode = st.sidebar.checkbox("Select all episodes")
if all_episode:
    episode_select = episode_container.multiselect("Select one or more episodes:",
         sorted_episode,sorted_episode)
else:
    episode_select =  episode_container.multiselect("Select one or more episodes:",
        sorted_episode,['EP825','EP727'])


list_of_ep = ' + '.join(map(str,episode_select))
#include unassigned
unassigned = st.sidebar.checkbox("Include unassigned", False)
if unassigned:

    df['COMP_ARTIST'] = df['COMP_ARTIST'].fillna('Not Assigned')


#select artists
filt_ep_artist = df[(df.Episode.isin(episode_select))]

sorted_artist = list(filt_ep_artist['COMP_ARTIST'].fillna('Not Assigned').unique())

artist_container = st.sidebar.container()
all_artist = st.sidebar.checkbox("Select all comp artists", True)

if all_artist:
    selected_artist = artist_container.multiselect("Select one or more comp artists:",
         sorted_artist,sorted_artist)
else:
    selected_artist =  artist_container.multiselect("Select one or more comp artists:",
        sorted_artist)


#status_filter

df.final = df
#main Filters
df.filt_ep = df[(df.Episode.isin(episode_select)) & (df.COMP_ARTIST.isin(selected_artist))]
df.not_moved = df.filt_ep[(df.filt_ep.LIT_STATUS != 'READY FOR COMP')]
df.filt_not_assigned = df.filt_ep[(df.filt_ep['LIT_STATUS'] == 'READY FOR COMP') & (df.filt_ep['COMP_ARTIST'] == 'Not Assigned')]
df.filt_master = df.filt_ep[(df.filt_ep['Type'] == 'MASTER')]
df.threedc = df.filt_ep[(df.filt_ep.COMP_STATUS == 'LIT 3DC')
                       |(df.filt_ep.COMP_STATUS == 'LIT 3DC RENDER')
                       |(df.filt_ep.COMP_STATUS == 'LIT 3DC RENDER DONE')
                       |(df.filt_ep.COMP_STATUS == 'FX 3DC')]
df.filt_assigned_shots = df.filt_ep.dropna(subset=['COMP_ARTIST'])
df.filt_on_floor = df.filt_assigned_shots[(df.filt_assigned_shots['COMP_STATUS'] != 'LIT 3DC')
                                        & (df.filt_assigned_shots['COMP_STATUS'] != 'LIT 3DC RENDER')
                                        & (df.filt_assigned_shots['COMP_STATUS'] != 'FX 3DC')
                                        & (df.filt_assigned_shots['COMP_STATUS'] != 'TO CHECK')
                                        & (df.filt_assigned_shots['FINAL_STATUS'] != 'DONE')]
df.filt_pending_review = df.filt_ep[(df.filt_ep['COMP_STATUS'] == 'TO CHECK') & (df.filt_ep['FINAL_STATUS'] != 'DONE') ]
df.not_done = df.filt_ep[(df.filt_ep['FINAL_STATUS'] != 'DONE')]
df.done = df.filt_ep[(df.filt_ep['FINAL_STATUS'] == 'DONE')]
df.filt_attempted = df.filt_ep[(df.filt_ep ['LIT_STATUS'] == 'READY FOR COMP')
                                    &  (df.filt_ep.COMP_STATUS.notnull())]
df.reviewed = df.filt_ep[(df.filt_ep ['LIT_STATUS'] == 'READY FOR COMP' ) &  (df.filt_ep.FINAL_STATUS.notnull())]
df.not_reviewed = df.filt_ep[(df.filt_ep ['LIT_STATUS'] == 'READY FOR COMP' )& (df.filt_ep['FINAL_STATUS'] != 'INT CORR') & (df.filt_ep['FINAL_STATUS'] != 'DONE')]
df.int_cor = df.filt_ep[(df.filt_ep ['LIT_STATUS'] == 'READY FOR COMP' )& (df.filt_ep['FINAL_STATUS'] == 'INT CORR')]
df.filt_untouched = df.filt_ep[(df.filt_ep ['LIT_STATUS'] == 'READY FOR COMP')
                                    &  (df.filt_ep.COMP_STATUS.isnull())& (df.filt_ep['FINAL_STATUS'] != 'DONE')]
df.final = df.filt_ep

#setup of sidebar elements

#write summary
st.write('All shots:', str(len(df.filt_ep['Episode']))
        ,'| Not ready of comp:', str(len(df.not_moved['Episode']))
        ,'| Done:', str(len(df.done['Episode']))
        ,'| Not Done:', str(len(df.not_done['Episode']))
        ,'| 3DC:', str(len(df.threedc['Episode']))
        ,'| To Check:', str(len(df.filt_pending_review['Episode']))
        ,'| On Floor:', str(len(df.filt_on_floor['Episode']))
        ,'| Attempted:', str(len(df.filt_attempted['Episode']))
        ,'| Reviewed:', str(len(df.reviewed['Episode']))
        ,'| Not reviewed:', str(len(df.not_reviewed['Episode']))
        ,'| Internal Correction:', str(len(df.int_cor['Episode']))
        ,'| Untouched:', str(len(df.filt_untouched['Episode']))
        ,'| Unassigned:', str(len(df.filt_not_assigned['Episode'])))
if status_selection == 'All Shots':
    df.final = df.filt_ep
    st.subheader('Showing all shots, Total count is '+ str(len(df.final['Episode'])))


if status_selection == 'Not ready of comp':
    df.final = df.not_moved
    st.subheader('Showing not ready of comp, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'Done':
    df.final = df.done
    st.subheader('Showing done shots, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'Not Done':
    df.final = df.not_done
    st.subheader('Showing not done shots, Total count is '+ str(len(df.final['Episode'])))

if status_selection == '3DC':
    df.final = df.threedc
    st.subheader('Showing 3DC shots, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'To Check':
    df.final = df.filt_pending_review
    st.subheader('Showing shots to check, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'On Floor':
    df.final = df.filt_on_floor
    st.subheader('Showing shots on floor, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'Attempted':
    df.final = df.filt_attempted
    st.subheader('Showing attempted shots, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'Reviewed':
    df.final = df.reviewed
    st.subheader('Showing reviewed shots, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'Not reviewed':
    df.final = df.not_reviewed
    st.subheader('Showing not reviewed shots, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'Internal Correction':
    df.final = df.int_cor
    st.subheader('Showing internal correction shots, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'Untouched':
    df.final = df.filt_untouched
    st.subheader('Showing internal correction shots, Total count is '+ str(len(df.final['Episode'])))

if status_selection == 'Not assigned':
    df.final = df.filt_not_assigned
    st.subheader('Showing not assigned shots, Total count is '+ str(len(df.final['Episode'])))

#st.sidebar.subheader('Bar settings')

status_slot = st.empty()
colour_slot = st.empty()
center_slot = st.empty()
path_selection_list = ['FINAL_STATUS','COMP_STATUS','COMP_ARTIST','LIT_STATUS','SHOT_INDEX','Episode']
path_selection = path_selection_list

#centric = st.sidebar.selectbox('Select base', ['Episode centric','Artist centric','Comp status centric','Final status centric'])

#---adding first column
#st.write(df.final)
acol1,acol2,acol3=  st.columns([1,1,.5])
with acol1:
    path_selection_list1 = ['COMP_ARTIST','FINAL_STATUS','COMP_STATUS','LIT_STATUS','Episode','SHOT_INDEX']
    sel_1 = st.selectbox('Select data', path_selection_list1)
    #st.write(px.bar(df.final.fillna('NO ENTRY'), x='COMP_STATUS', y='FRAMES', color='COMP_ARTIST',
             #facet_col='Episode', facet_row='FINAL_STATUS', hover_data = [df.final.index],width=500, height=750, color_discrete_map={'Not Assigned': 'black'},
             #category_orders={'Episode': ['Episode'],'FINAL_STATUS': ['FINAL_STATUS']}))

    st.write(px.histogram(df.final.fillna('NO ENTRY'), y='FRAMES', x= sel_1, hover_data = [df.final.index], color= color, width=600, height=750))

with acol2:
    path_selection_list2 = ['COMP_STATUS','FINAL_STATUS','COMP_ARTIST','LIT_STATUS','Episode','SHOT_INDEX']
    sel_2 = st.selectbox('Select data', path_selection_list2)
    st.write(px.histogram(df.final.fillna('NO ENTRY'), y='FRAMES', x= sel_2, hover_data = ['shot_index'], color= color, width=600, height=750))

with acol3:
    path_selection_list3 = ['FINAL_STATUS','COMP_STATUS','COMP_ARTIST','LIT_STATUS','Episode','SHOT_INDEX']
    sel_3 = st.selectbox('Select data', path_selection_list3)
    st.write(px.histogram(df.final.fillna('NO ENTRY'), y='FRAMES', x= sel_3, hover_data = ['shot_index'], color= color, width=300, height=750))
    

#adding page selection



#


st.write(df.final)
# setup auto refresh
input_sec = 10
def countdown(time_sec,divide):

        while time_sec:

            mins, secs = divmod(time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            my_slot.write('Refresh in: '+timeformat, end='\r')
            time.sleep(1)
            time_sec -= 1
            my_bar.progress(time_sec*divide)


        my_slot.write("Refreshing...")
if auto:

    my_bar = my_slot2.progress(0)

    progres_divide = input_sec/100


    countdown(input_sec,progres_divide)
    st.legacy_caching.clear_cache()
    st.experimental_rerun()
