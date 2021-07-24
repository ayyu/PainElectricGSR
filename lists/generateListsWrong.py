import pandas as pd
import numpy as np
import random
from itertools import groupby

n_runs = 10
n_trials = 6
iti_min = 2
iti_max = 3
n_levels = 6
stimuli = ["pain", "electric"]
levels = np.arange(1, n_levels+1)

max_cons_repeats = 2
max_first_trial = levels[-2]
max_diff_levels = 3

print("brute force generating list...")

def validate_run_list(run_list):
    for run in run_list:
        stimuli = [trial[0] for trial in run]
        levels = [trial[1] for trial in run]
        consecutive_repeats = [sum(1 for i in group) for i, group in groupby(stimuli)]
        diff_levels = np.diff(levels)
        if max(consecutive_repeats) > max_cons_repeats:
            print('too many repeated consecutive modalities')
            print(consecutive_repeats)
            return False
        if levels[0] >= max_first_trial:
            print('initial trial level too high')
            print(levels[0])
            return False
        if max(abs(diff_levels)) > max_diff_levels:
            print('difference between consecutive trials too high')
            print(diff_levels)
            return False
    return True

conditions = [[stimulus, level] for stimulus in stimuli for level in levels]
trial_list = conditions * int(n_runs * n_trials / len(conditions))

reqs_met = False

run_list = []

#while not reqs_met:
#    for i_run in range(n_runs):       
#    random.shuffle(trial_list)
#    run_list = [trial_list[n:n+n_trials] for n in range(0, len(trial_list), n_trials)]
#    reqs_met = validate_run_list(run_list)

random.shuffle(trial_list)
run_list = [trial_list[n:n+n_trials] for n in range(0, len(trial_list), n_trials)]

print("saving runs with randomized ITI jitter")

itis = np.linspace(iti_min, iti_max, n_trials)

for i_run in range(1, n_runs+1):
    random.shuffle(itis)
    run = run_list[i_run-1]
    run_stimuli = [trial[0] for trial in run]
    run_levels = [trial[1] for trial in run]
    data = [[1, "", "TrialProc", stimulus, level, iti] for stimulus, level, iti in \
        zip(run_stimuli, run_levels, itis)]
    df = pd.DataFrame(data, columns=["Weight", "Nested", "Procedure", "Modality", "Level", "ITI"])
    df.to_csv("run-%d.txt" % i_run, sep="\t", index=False)