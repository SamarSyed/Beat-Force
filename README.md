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
