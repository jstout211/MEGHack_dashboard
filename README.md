# MEGHack_dashboard

## Objective build an interactive dashboard for MEG results

## Install - (full mne required because of 3D viz)
```
mamba create --override-channels --channel=conda-forge --name=megDash mne -y  
conda activate megDash
mamba install --channel=conda-forge pip pandas statsmodels shiny
```

## Test data
```
data = pd.read_csv('./data/TESTDATA.csv')
```
