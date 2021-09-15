#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import pandas as pd
# import numpy as np
# import pickle
# import os

from HMM_modeling import HMM, make_sequence, train_HMM

import numpy as np
import pandas as pd
import librosa
import json
import pickle
from zipfile import ZipFile
import os
import soundfile as sf
import audioread
from pydub import AudioSegment
import shutil



#Main Function:

def beat_map_generator(song_path, song_name, difficulty, model, k=5, version = 2):
    
    if model == 'HMM':
        HMM_mapper(song_path, song_name, difficulty, version = version)
    else:
        print('Please choose a model for the mapping.')

#Basic File Writing Functions
def write_info_file(song_name, bpm, difficulty):
    """This function creates the 'info.dat' file that needs to be included in the beatamp zip file."""

    difficulty_rank = None
    jump_movement = None
    if difficulty.casefold() == 'easy'.casefold():
        difficulty_rank = 1
        jump_movement = 8
        diff_name = 'Easy'
    elif difficulty.casefold() == 'normal'.casefold():
        difficulty_rank = 3
        jump_movement = 10
        diff_name = 'Normal'
    elif difficulty.casefold() == 'hard'.casefold():
        difficulty_rank = 5
        jump_movement = 12
        diff_name = 'Hard'
    elif difficulty.casefold() == 'expert'.casefold():
        difficulty_rank = 7
        jump_movement = 14
        diff_name = 'Expert'
    elif difficulty.casefold() == 'expertPlus'.casefold():
        difficulty_rank = 9
        jump_movement = 16
        diff_name = 'ExpertPlus'
            
    info = {'_version': '2.0.0',
            '_songName': f"{song_name}",
            '_songSubName': '',
            '_songAuthorName': '',
            '_levelAuthorName': 'Beat Force',
            '_beatsPerMinute': round(bpm),
            '_songTimeOffset': 0,
            '_shuffle': 0,
            '_shufflePeriod': 0,
            '_previewStartTime': 10,
            '_previewDuration': 30,
            '_songFilename': 'song.egg',
            '_coverImageFilename': 'cover.jpg',
            '_environmentName': 'DefaultEnvironment',
            '_customData': {},
             '_difficultyBeatmapSets': [{'_beatmapCharacteristicName': 'Standard',
                                         '_difficultyBeatmaps': [{'_difficulty': diff_name,
                                                                  '_difficultyRank': difficulty_rank,
                                                                  '_beatmapFilename': f"{difficulty}.dat",
                                                                  '_noteJumpMovementSpeed': jump_movement,
                                                                  '_noteJumpStartBeatOffset': 0,
                                                                  '_customData': {}}]}]}
    with open('info.dat', 'w') as f:
        json.dump(info, f)

def write_level(difficulty, events_list, notes_list, obstacles_list):
    """This function creates the 'level.dat' file that contains all the block placements and level data needed to play the level."""
    
    level = {'_version': '2.0.0',
             '_customData': {'_time': '',  
                             '_BPMChanges': [], 
                             '_bookmarks': []},
             '_events': events_list,
             '_notes': notes_list,
             '_obstacles': obstacles_list}
    with open(f"{difficulty}.dat", 'w') as f:
        json.dump(level, f)

def music_file_converter(song_path):
    """This function takes in an input song files and converts it into an acceptable format"""
    if song_path.endswith('.mp3'):
        AudioSegment.from_mp3(song_path).export('song.egg', format='ogg')
    elif song_path.endswith('.wav'):
        AudioSegment.from_wav(song_path).export('song.egg', format='ogg')
    elif song_path.endswith('.flv'):
        AudioSegment.from_flv(song_path).export('song.egg', format='ogg')
    elif song_path.endswith('.raw'):
        AudioSegment.from_raw(song_path).export('song.egg', format='ogg')
    elif song_path.endswith('.ogg') or song_path.endswith('.egg'):
        shutil.copy2(song_path, 'song.egg')
    else:
        print("Unsupported song file type. Choose a file of type .mp3, .wav, .flv, .raw, or .ogg.")

def zip_folder_exporter(song_name, difficulty):
    save_path = btn_SavePathClick()
    files = ['info.dat', f"{difficulty}.dat", 'cover.jpg', 'song.egg']
    path = os.path.join(save_path,f"{song_name}_{difficulty}.zip")
    print(path)
    with ZipFile(path, 'w') as custom:
        for file in files:
            print('test print',file)
            custom.write(file)
    for file in files:
        if file != 'cover.jpg':
            os.remove(file)


def beat_features(song_path):
    """This function takes in the song stored at 'song_path' and estimates the bpm and beat times."""
    #Load song and split into harmonic and percussive parts.
    y, sr = librosa.load(song_path)
    #Isolate beats and beat times
    bpm, beat_frames = librosa.beat.beat_track(y=y, sr=sr, trim = False)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return bpm, beat_times, y, sr

#Hidden Markov Models Mapping Functions
def HMM_mapper(song_path, song_name, difficulty, version = 2):
    """This function generates a beatmap with the trained Hidden Markov Models."""
    #Load song and get beat features
    print("Loading Song...")
    bpm, beat_times, y, sr = beat_features(song_path)
    beat_times = [x*(bpm/60) for x in beat_times] #list(range(len(beat_times)))
    print("Song loaded successfully!")
    #Write lists for note placement, event placement, and obstacle placement
    print("Mapping with Hidden Markov Model...")
    notes_list = HMM_notes_writer(beat_times, difficulty, version)
    events_list = []
    obstacles_list = [] # used later for obstacle and lightshow generation
    print("Mapping done!")
    #Write and zip files
    print("Writing files to disk...")
    write_info_file(song_name, bpm, difficulty)
    write_level(difficulty, events_list, notes_list, obstacles_list)
    print("Converting music file...")
    music_file_converter(song_path)
    print("Zipping folder...")
    zip_folder_exporter(song_name, difficulty)
    print("Finished! Look for zipped folder in your selected path, unzip the folder, and place in the 'CustomLevels' folder in the Beat Saber directory")

def sequence_to_df(walk):
    """Function for turning a Markov walk sequence into a DataFrame of note placement predictions"""
    sequence = []
    for step in walk:
        sequence.append(step.split(","))
    constant = ['notes_type_0', 'notes_lineIndex_0', 'notes_lineLayer_0',
                    'notes_cutDirection_0', 'notes_type_1', 'notes_lineIndex_1', 'notes_lineLayer_1', 
                    'notes_cutDirection_1', 'notes_type_3', 'notes_lineIndex_3',
                    'notes_lineLayer_3', 'notes_cutDirection_3']
    df = pd.DataFrame(sequence, columns = constant)
    return df

def HMM_notes_writer(beat_list, difficulty, version):
    """Writes a list of notes based on a Hidden Markov Model sequence."""
    #Load model
    if version == 1:
        with open(f"./models/HMM_{difficulty}.pkl", 'rb') as m:
            MC = pickle.load(m)
    elif version == 2:
        with open(f"./models/HMM_{difficulty}_v2.pkl", 'rb') as m:
            MC = pickle.load(m)
    #Set note placement rate dependent on difficulty level
    counter = 2
    beats = []
    rate = None
    if difficulty == 'easy':
        rate = 3
    elif difficulty == 'normal':
        rate = 2
    else:
        rate = 1
    while counter <= len(beat_list):
        beats.append(counter)
        counter += rate
    #Get HMM walk long enough to cover number of beats
    random_walk = MC.walk()
    while len(random_walk) < len(beats):
        random_walk = MC.walk()
    df_walk = sequence_to_df(random_walk)
    #Combine beat numbers with HMM walk steps
    df_preds = pd.concat([pd.DataFrame(beats, columns = ['_time']), df_walk], axis = 1, sort = True)
    df_preds.dropna(axis = 0, inplace = True)
    #Write notes dictionaries
    notes_list = []
    for index, row in df_preds.iterrows():
        for x in list(filter(lambda y: y.startswith('notes_type'), df_preds.columns)):
            if row[x] != '999':
                num = x[-1]
                note = {'_time': row['_time'],
                        '_lineIndex': int(row[f"notes_lineIndex_{num}"]),
                        '_lineLayer': int(row[f"notes_lineLayer_{num}"]),
                        '_type': num,
                        '_cutDirection': int(row[f"notes_cutDirection_{num}"])}
                notes_list.append(note)
   #Remove potential notes that come too early in the song:
    for i, x in enumerate(notes_list):
        if notes_list[i]['_time'] >= 0 and notes_list[i]['_time'] <= 1.5:
            del notes_list[i]
        elif notes_list[i]['_time'] > beats[-1]:
            del notes_list[i]

    return notes_list


def choose_rate(db, difficulty):
    """
    This function modulates the block placement rate by using the average amplitude (i.e., 'loudness') across beats to choose how many blocks per beat will be placed.
    """
    db = np.abs(db)
    p = None
    if difficulty.casefold() == 'easy'.casefold():
        if db > 70:
            p = [0.95, 0.05, 0, 0, 0, 0]
        elif db <= 70 and db > 55:
            p = [0.90, 0.10, 0, 0, 0, 0]
        elif db <= 55 and db > 45:
            p = [0.80, 0.2, 0, 0, 0, 0]
        elif db <= 45 and db > 35:
            p = [0.4, 0.5, 0.1, 0, 0, 0]
        else:
            p = [0.3, 0.6, 0.1, 0, 0, 0]
    elif difficulty.casefold() == 'normal'.casefold():
        if db > 70:
            p = [0.95, 0.05, 0, 0, 0, 0]
        elif db <= 70 and db > 55:
            p = [0.5, 0.5, 0, 0, 0, 0]
        elif db <= 55 and db > 45:
            p = [0.3, 0.7, 0, 0, 0, 0]
        elif db <= 45 and db > 35:
            p = [0.2, 0.7, 0.1, 0, 0, 0]
        else:
            p = [0.05, 0.7, 0.25, 0, 0, 0]
    elif difficulty.casefold() == 'hard'.casefold():
        if db > 70:
            p = [0.95, 0.05, 0, 0, 0, 0]
        elif db <= 70 and db > 55:
            p = [0.5, 0.5, 0, 0, 0, 0]
        elif db <= 55 and db > 45:
            p = [0.2, 0.6, 0.2, 0, 0, 0]
        elif db <= 45 and db > 35:
            p = [0.1, 0.5, 0.4, 0, 0, 0]
        else:
            p = [0.05, 0.35, 0.6, 0, 0, 0]
    elif difficulty.casefold() == 'expert'.casefold():
        if db > 70:
            p = [0.8, 0.2, 0, 0, 0, 0]
        elif db <= 70 and db > 55:
            p = [0.2, 0.7, 0.1, 0, 0, 0]
        elif db <= 55 and db > 50:
            p = [0.1, 0.4, 0.3, 0.2, 0, 0]
        elif db <= 50 and db > 45:
            p = [0, 0.05, 0.6, 0.35, 0, 0]
        else:
            p = [0, 0, 0.35, 0.65, 0, 0]
    elif difficulty.casefold() == 'expertPlus'.casefold():
        if db > 70:
            p = [0, 0.5, 0.4, 0.1, 0, 0]
        elif db <= 70 and db > 55:
            p = [0, 0.3, 0.6, 0.1, 0, 0]
        elif db <= 55 and db > 50:
            p = [0, 0.1, 0.6, 0.3, 0, 0]
        elif db <= 50 and db > 45:
            p = [0, 0.05, 0.1, 0.6, 0.25, 0]
        else:
            p = [0, 0, 0, 0.5, 0.3, 0.2]
    return np.random.choice([0, 1, 2, 4, 8, 16], p = p)

def amplitude_rate_modulation(y, sr, difficulty):
    """This function uses the average amplitude (i.e., 'loudness') of a beat and the difficulty level to determine 
    how many blocks will be placed within the beat. Returns a list of beat numbers."""
    #Make amplitude matrix
    D = np.abs(librosa.stft(y))
    db = librosa.amplitude_to_db(D, ref=np.max)
    #Get beat frames and sync with amplitudes
    tempo, beat_frames = librosa.beat.beat_track(y, sr, trim = False)
    beat_db = pd.DataFrame(librosa.util.sync(db, beat_frames, aggregate = np.mean))
    #Mean amplitude per beat
    avg_beat_db = beat_db.mean()
    #Choose rates and smooth rate transitions
    rates = [0]
    counter = 1
    while counter < len(avg_beat_db)-1:
        rate = choose_rate(np.mean([avg_beat_db.iloc[counter-1], avg_beat_db.iloc[counter], avg_beat_db.iloc[counter+1]]), difficulty)
        diff = np.abs(rate - rates[-1])
        if difficulty.casefold() == 'expert'.casefold():
            maxdiff = 4
        elif difficulty.casefold() == 'expertPlus'.casefold():
            maxdiff = 8
        else:
            maxdiff = 2
        while diff > maxdiff:
            rate = choose_rate(np.mean([avg_beat_db.iloc[counter-1], avg_beat_db.iloc[counter], avg_beat_db.iloc[counter+1]]), difficulty)
            diff = rates[-1] - rate
        if rate == 4 and rates[-1] == 4: #and rates[-2] == 4:
            rate = np.random.choice([0, 1, 2])
        rates.append(rate)
        counter +=1
    #Make list of beat numbers based on rates
    beat_num_list = []
    for ind, val in enumerate(rates):
        if val == 0:
            continue
        elif val == 1:
            beat_num_list.append(ind)
        else:
            num_list = [ind, ind+1]
            for x in range(1, val):
                num_list.append(ind+(x/val))
            for y in num_list:
                beat_num_list.append(y)
    beat_num_list = list(set(beat_num_list))
    beat_num_list.sort()
    return beat_num_list
  


import eel
from tkinter import *
from tkinter import filedialog

eel.init('web')

@eel.expose
def btn_ResimyoluClick():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    filepath = filedialog.askopenfilename() #TODO: Add file type restrcition
    return filepath

@eel.expose
def btn_SavePathClick():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder = filedialog.askdirectory() #TODO: Add file type restrcition
    return folder

@eel.expose
def generate(song_path, difficulty):
    head, tail = os.path.split(song_path)
    song_name = os.path.splitext(tail)[0]
    print("success: got follwing song path" + song_path)
    # return "success: got follwing song path" + song_path
    beat_map_generator(song_path, song_name, difficulty, 'HMM', k=5, version = 2)
    return "success"

@eel.expose
def dummy(param):
    head, tail = os.path.split(param)
    song_name = tail
    # song_name = os.path.splitext(tail)[0]
    return song_name



# beat_map_generator("Funky-Town-Playa-Phonk.ogg", 'funky town HMM v2', 'expertPlus', 'HMM', k=5, version = 2)


# In[ ]:


eel.start('index.html', size=(1000, 600))

