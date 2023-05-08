# MEGHack_dashboard

## Objective build an interactive dashboard for MEG results

## Install - (full mne required because of 3D viz)
```
mamba create --override-channels --channel=conda-forge --name=megDash mne -y  
conda activate megDash
mamba install -n megDash --override-channels  -c conda-forge statsmodels shiny

git clone https://github.com/jstout211/MEGHack_dashboard.git
pip install -e ./MEGHack_dashboard  #This allows the data directory to be referenced locally 
```

## To run 
`shiny run --reload megdash/app.py` <br>
In a webrowser `localhost:8000` (8000 is typical, but if different read the terminal output)


## Test data
`data = pd.read_csv('./megdash/data/TESTDATA.csv')` <br><br>
OR <br>
```
import megdash
import os.path as op
data_fname = op.join(megdash.__path__[0], 'data', 'TESTDATA.csv')
data = pd.read_csv(data_fname)
```
