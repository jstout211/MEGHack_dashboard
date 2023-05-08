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

## Test data
```
data = pd.read_csv('./data/TESTDATA.csv')
```
