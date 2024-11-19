#!/usr/bin/env python3
"""Make the CMSInterferenceFunc scaling input data for all channels

Run the command with:
python3 makeinterference.py

Run 1D scans with also building the workspace with:
python3 makeinterference.py workspace

Add `-a` for Asimov data run, add `-ns` for fits without systematics

"""

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import uproot
from matplotlib import pyplot as plt

all_wcs = [
    "cQQ1",
    "cQei",
    "cQl3i",
    "cQlMi",
    "cQq11",
    "cQq13",
    "cQq81",
    "cQq83",
    "cQt1",
    "cQt8",
    "cbW",
    "cpQ3",
    "cpQM",
    "cpt",
    "cptb",
    "ctG",
    "ctW",
    "ctZ",
    "ctei",
    "ctlSi",
    "ctlTi",
    "ctli",
    "ctp",
    "ctq1",
    "ctq8",
    "ctt1",
]

wc_ranges = {
    "cQQ1": (-6.0, 6.0),
    "cQei": (-4.0, 4.0),
    "cQl3i": (-5.5, 5.5),
    "cQlMi": (-4.0, 4.0),
    "cQq11": (-0.7, 0.7),
    "cQq13": (-0.35, 0.35),
    "cQq81": (-1.7, 1.5),
    "cQq83": (-0.6, 0.6),
    "cQt1": (-6.0, 6.0),
    "cQt8": (-10.0, 10.0),
    "cbW": (-3.0, 3.0),
    "cpQ3": (-4.0, 4.0),
    "cpQM": (-15.0, 20.0),
    "cpt": (-15.0, 15.0),
    "cptb": (-9.0, 9.0),
    "ctG": (-0.8, 0.8),
    "ctW": (-1.5, 1.5),
    "ctZ": (-2.0, 2.0),
    "ctei": (-4.0, 4.0),
    "ctlSi": (-5.0, 5.0),
    "ctlTi": (-0.9, 0.9),
    "ctli": (-4.0, 4.0),
    "ctp": (-15.0, 40.0),
    "ctq1": (-0.6, 0.6),
    "ctq8": (-1.4, 1.4),
    "ctt1": (-2.6, 2.6),
}

def run_workspace():

    cmd = (
        "text2workspace.py combinedcard.txt -P HiggsAnalysis.CombinedLimit.InterferenceModels:interferenceModel"
        " --PO scalingData=scalings.json --PO verbose -o workspace_interference.root"
    )
    subprocess.call(cmd.split())
    print("finish workspace making, running fits")

def run_1Dscans():
    wcranges = ":".join(f"{wc}={wc_ranges[wc][0]},{wc_ranges[wc][1]}" for wc in all_wcs)

    # whether to fix all other WCs or profile them
    scan = f"--algo grid --floatOtherPOIs 0 --setParameterRanges {wcranges} --points 30"  # 1D scans with systematics

    if "-a" in sys.argv:
        scan += " -t -1 --setParameters ctW=0,ctZ=0,ctp=0,cpQM=0,ctG=0,cbW=0,cpQ3=0,cptb=0,cpt=0,cQl3i=0,cQlMi=0,cQei=0,ctli=0,ctei=0,ctlSi=0,ctlTi=0,cQq13=0,cQq83=0,cQq11=0,ctq1=0,cQq81=0,ctq8=0,ctt1=0,cQQ1=0,cQt8=0,cQt1=0"

    if "-ns" in sys.argv:
        scan += " --freezeParameters allConstrainedNuisances"

    print("running interference fits")
    tic = time.monotonic()
    for wc in all_wcs:
        cmd = f"combine -M MultiDimFit {scan} -P {wc} workspace_interference.root -n .scan.float0.IM.withsys.{wc}"
        subprocess.call(cmd.split())
    toc = time.monotonic()
    print(f"CMSInterferenceFunc approach: {toc-tic:.1f}s")

    fig, axes = plt.subplots(13, 2, figsize=(8, 13 * 4))

    print(f"making plots...")
    for wc, ax in zip(all_wcs, axes.reshape(-1)):
        filename = f"higgsCombine.scan.float0.IM.withsys.{wc}.MultiDimFit.mH120.root"
        me = uproot.open(filename)["limit"].arrays([wc, "deltaNLL"], entry_start=1)

        ax.set_title(wc)
        ax.plot(me[wc], me.deltaNLL, label="IM", linestyle="--")
        ax.legend()

    fig.savefig("1Dscan_26wc_float0_IM_withsys.pdf")


if __name__ == "__main__":
    if "workspace" in sys.argv:
        run_workspace()
    run_1Dscans()
    print("Done")


