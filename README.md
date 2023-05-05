# MEGHack_dashboard

## Objective build an interactive dashboard for MEG results

## Install - (full mne required because of 3D viz)
```
mamba create -n megDash --channel=conda-forge mne pip pandas statsmodels 
mamba install -c conda-forge shiny
```

## Test data
```
data = pd.read_csv('./data/TESTDATA.csv')
```
