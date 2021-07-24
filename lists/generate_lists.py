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
max_first_trial = levels[-3]
max_diff_levels = 3

print("generating list pseudorandomly...")

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
        if levels[0] > max_first_trial:
            print('initial trial level too high')
            print(levels[0])
            return False
        if max(abs(diff_levels)) > max_diff_levels:
            print('difference between consecutive trials too high')
            print(diff_levels)
            return False
    return True

conditions = [(stimulus, level) for stimulus in stimuli for level in levels]
trial_list = conditions * int(n_runs * n_trials / len(conditions))

runs_stimuli = [[""]*n_trials for i in range(n_runs)]
runs_levels = [[0]*n_trials for i in range(n_runs)]

reqs_met = False
while not reqs_met:
    reqs_met = True
    random.shuffle(trial_list)
    stimuli_list = [trial[0] for trial in trial_list]
    level_list = [trial[1] for trial in trial_list]
    for i_trial in range(n_trials):
        for i_run in range(n_runs):
            if i_trial == 0:
                idx_legal = [i for i, e in enumerate(level_list) if e <= max_first_trial]
            else:
                idx_legal_level = [i for i, e in enumerate([abs(level - runs_levels[i_run][i_trial-1]) for level in level_list]) \
                    if e <= max_diff_levels]
                if (i_trial > 1):
                    idx_legal_stimuli = [i for i, e in enumerate(stimuli_list) \
                        if not e == runs_stimuli[i_run][i_trial-1] == runs_stimuli[i_run][i_trial-2]]
                    idx_legal = list(set(idx_legal_level) & set(idx_legal_stimuli))
                else:
                    idx_legal = idx_legal_level
            if not idx_legal:
                print("failed attempt")
                reqs_met = False
                break
            runs_levels[i_run][i_trial] = level_list.pop(idx_legal[0])
            runs_stimuli[i_run][i_trial] = stimuli_list.pop(idx_legal[0])
        if not reqs_met:
            break

run_list = [[(stimulus, level) for stimulus, level in zip(stimuli, levels)] \
    for stimuli, levels in zip(runs_stimuli, runs_levels)]

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