#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import pickle
import markovify
import os
# from tqdm.notebook import tqdm


# In[5]:




def make_sequence(df):
    """Returns a sequence that describe the placement and type of blocks for use in a HMM generator."""
    df_notes = df.iloc[:, 13:]
    df_notes.drop(index = df_notes[(df_notes == 999).all(axis = 1)].index, axis = 0, inplace = True)
    df_notes.reset_index(drop = True, inplace = True)
    seq = []
    for index, row in df_notes.iterrows():
        values = {}
        for x in df_notes.columns:
            values.update({x: int(row[x])})
        if 'notes_type_3' not in list(values.keys()):
            values.update({'notes_type_3': 999})
            values.update({'notes_lineIndex_3': 999})
            values.update({'notes_lineLayer_3': 999})
            values.update({'notes_cutDirection_3': 999})
        elif 'notes_type_0' not in list(values.keys()):
            values.update({'notes_type_0': 999})
            values.update({'notes_lineIndex_0': 999})
            values.update({'notes_lineLayer_0': 999})
            values.update({'notes_cutDirection_0': 999})
        elif 'notes_type_1' not in list(values.keys()):
            values.update({'notes_type_1': 999})
            values.update({'notes_lineIndex_1': 999})
            values.update({'notes_lineLayer_1': 999})
            values.update({'notes_cutDirection_1': 999})
        word = f"{values['notes_type_0']},{values['notes_lineIndex_0']},{values['notes_lineLayer_0']},{values['notes_cutDirection_0']},{values['notes_type_1']},{values['notes_lineIndex_1']},{values['notes_lineLayer_1']},{values['notes_cutDirection_1']},{values['notes_type_3']},{values['notes_lineIndex_3']},{values['notes_lineLayer_3']},{values['notes_cutDirection_3']}"
        seq.append(word)
    return seq

def generate_corpus(difficulty):
    """This function generates a corpus of sequences for training a HMM with markovify for a chosen difficulty level."""
    corpus = []
    filelist = [f for f in os.listdir('./data/processed_data/')]
    for f in tqdm(filelist):
        if f.endswith(f"{difficulty}.pkl"):
            with open(f"./data/processed_data/{f}", 'rb') as d:
                df = pickle.load(d)
            seq = make_sequence(df)
            corpus.append(seq)
    return corpus

def train_HMM(corpus):
    """This function trains the HMM given a corpus of sequences."""
    MC = markovify.Chain(corpus, 5)
    return MC

def HMM(difficulty):
    """Top level function for building a corpus and training a HMM all in one."""
    corpus = generate_corpus(difficulty)
    print("Corpus generated")
    MC = train_HMM(corpus)
    return MC



# In[9]:


# difficulties = ['easy', 'normal', 'hard', 'expert', 'expertPlus']
# for difficulty in difficulties:
#     MC = HMM(difficulty)
# #     print("write file")
# #     print(r"C:\Users\Oculus VR\Desktop\BeatMapSynthesizer-master\models\HMM_{}_v2.pkl".format(difficulty))
#     with open(r"C:\Users\Oculus VR\Desktop\BeatMapSynthesizer-master\models\HMM_{}_v2.pkl".format(difficulty), 'wb') as f:
#         pickle.dump(MC, f)


# In[ ]:




