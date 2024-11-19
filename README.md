# EFTFit-v2.0

This branch is created to run the basics of EFTFit with interference model compatible with [CMSSW14x](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/#installation-instructions).
## Set up
#### Install CMSSW14

The most recent cms environment is made compatible with upgraded machine system el9. Run the following commands to install:
```
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
```
#### Get combine v10
```
cd CMSSW_14_1_0_pre4/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v10.0.2
scramv1 b clean; scramv1 b # always make a clean build
```

#### Install EFTFit-v2
Inside `CMSSW_14_1_0_pre4/src`, get the current version of EFTFit-v2
```
cmsenv
git clone https://github.com/ywan2/EFTFit-v2.git
scram b -j8
```

## Run combine
#### Get necessary files
Move the the datacard root and text files, along with `scalings.json` file made from [topeft repo](https://github.com/TopEFT/topeft.git) to `EFTFit-v2/scripts/`.
Make the combined text card with command:
```
combineCards.py ttx_multileptons-*.txt > combinedcard.txt
```
You should eventually have 1. combinedcard.txt, 2. scalings.json, and 3. all datacards for the next steps.

#### One script to run all
In `scripts` directory, python script `Run_1DScans_IM.py` includes all everything we need to run: build workspace, 1D fit scans, and 1D scan plots.
Simply run this command:
```
cd scripts/
python3 Run_1DScans_IM.py workspace
```
## More details
#### Add parameters
If you already have the workspace ready, and want to make 1D scans with Asimov data, run:
```
python3 Run_1DScans_IM.py -a
```
If to exclude systematics in the fits, run:
```
python3 Run_1DScans_IM.py -ns
```
So far the combine root files are hardcoded in naming in the script so one needs to edit it accordingly to avoid overwriting.

#### Build workspace alone
To individually make the workspace with interference model without making the scans and plots, the command is:
```
text2workspace.py combinedcard.txt -P HiggsAnalysis.CombinedLimit.InterferenceModels:interferenceModel --PO scalingData=scalings.json --PO verbose -o workspace_interference.root
```
