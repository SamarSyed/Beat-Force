# Beat-Force
This is the Serious Games Project Submission Group P10 SS2021

This project uses Anaconda Environments. 
> Anaconda is a distribution of the Python and R programming languages for scientific computing (data science, machine learning applications, large-scale data processing, predictive analytics, etc.), that aims to simplify package management and deployment.

If not already done so, please install Anaconda by following the usual steps described in this link: https://www.anaconda.com/products/individual-d

## Set up the project
To set up the project please clone or download this repository to your local harddrive.
Afterwards, please download the trained models from the following link and put them into the "models" folder of this project: https://drive.google.com/drive/folders/16WW3Iro3xEdSNNtVobxLE2SBeqb9XWVE?usp=sharing

To activate the environment, open the Anaconda Prompt as administrator, change into the Beat Force directory (into location of the downloaded repository) and 
execute the following commands:

```
conda env create --file beatforce.yml
conda activate beatforce
```

To start the Beat Force app just type the following command into the open Anaconda Prompt:

```
python MapGeneration.py
```

If setting up the environment does not work, you can simply install all needed libraries using the `requirements.txt` file and the pip installer for python.
Just execute the following command in windows cmd after changing into the project directory:

```
pip install -r requirements.txt
```
## Structure of the project

The contains the following files and folders:
`envs` folder: stores the environment information for the Anaconda environment for this project
`models` folder: stores the trained Hidden Markov Models, one model for each difficulty level
`Test Songs` folder: contains some songs in .mp3 format that can be used to test the Beat Force app
`web` folder: contains all files and folders relevant to the UI
`HMM_modeling.py`: defines function for training the HMM models as well as predicting with the trained models
`Map Generation.py`: is the main file for this project which contains the high level functions to take in an input song, preprocess it, generate a beatmap, pack it into a zip file and communicate with the UI
`README.md`: describes how to set up and use the project
`beatforce.ico`: is the icon for the Beat Force app
`beatforce.yml`: is the Anaconda environment file that contains information about the installed packages
`cover.jpg`: is the cover picture for generated beatmaps
`requirements.txt`: is the requirements file containing a list of all necessary libraries for the project
