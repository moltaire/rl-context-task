<p align='center'><img src="stim/images/Set 1/10.png" alt="Reinforcement" width="20%" height="auto"><img src="stim/images/Set 1/9.png" alt="Learning" width="20%" height="auto"><img src="stim/images/Set 1/1.png" alt="Is" width="20%" height="auto"><img src="stim/images/Set 1/4.png" alt="Fun" width="20%" height="auto"></p>

# Context-Dependent Reinforcement-Learning Task

The repository replicates the task described in Gueguen et al. (2024) in PsychoPy. Different variants of this task are also used and described in Bavard et al. (2021).

## Details

### Conditions

Conditions (i.e., trial information) is specified in `stim/conditions.csv`.  
Note that the task currently does not automatically create rewards and manage reward probabilities. All of this work and logic needs to be provided in the `conditions.csv` file for now. While this is a bit more tedious, it allows for a great level of control over what is shown. In the future, a script creating the `conditions.csv` file can be used to implement different task variants.

#### Columns in `conditions.csv`

The conditions-file should have the following columns:
- `phase`: This specifies the task phase. Accepted values are:
  - `"training"`: Trials in this phase don't count towards total points tally and can be repeated up to `training_n_repeats_max` times. They use a separate set of symbols (identified by `symbol1` and `symbol2` values - see below - starting with `"T"`)
  - `"learning"`: Trials in this phase count towards total points tally. They use `symbol` values `"A"`, `"B"`, etc.
  - `"transfer"`: Technically, can be identical to the `learning` phase, but will accept a different set of instructions, and, for example, different symbol pairings or `feedback` conditions (see below)
  - `"explicit"`: In this phase, no symbols are shown. Instead `probability` and `outcome` are shown explicitly for each option. 
- `block`: This allows for splitting phases into blocks. If `show_block_dividers` is set to `True`, break screens will be included. Block values can re-start within every `phase`. Note that the `temporal_arrangement` setting that shuffles trials or trial blocks (based on `trial_type`, see below) applies within each block.
- `trial_id`: A running ID for trials. They are written into the data, they're not used for anything else.
- `trial_type`: This variable is used to determine the `temporal_arrangement` setting. Within each block, if `temporal_arrangement` is set to `"interleaved"`, all trial types are shuffled randomly. In contrast, if `temporal_arrangement` is set to `"blocked"`, trials with the same `trial_type` remain chunked together, but the chunk order is shuffled.
- `symbol1`, `symbol2`: These specify the symbols shown for each trial. Training symbols are denoted with `T` (e.g., `T1`). Task symbols are denoted with uppercase letters `A`, `B`, etc. Note, that the task will map different symbols (i.e., image files) to these symbol IDs for each run.
- `option1pos`: Denotes the position (`left` or `right`) of option 1. Option 2 will take the other position.
- `feedback`: Sets the feedback condition. This lets you change behavior in `transfer` and `explicit` phases. Accepted values are:
  - `"complete"`: Outcomes of both options (chosen and unchosen) are shown.
  - `"partial"`: Outcome of the chosen option is shown. Unchosen outcome is shown as "?"
  - `"none"`: Both outcomes are shown as "?"
  - `"skip"`: Feedback phase is skipped completely
- `outcome_randomness`: Allows you to determine if option outcomes are realized truly random, according to specified probabilities in each trial (see below), or pseudorandomly, where you predefine the outcomes in the `actual_outcome` columns (see below).
  - `"random"`: Each option's realized outcome will be drawn truly randomly. For example, the outcome in column `potential_outcome1` will be realized with probability given in the `probability1` column, or 0 otherwise.
  - `"pseudorandom"`: Each option's realized outcome in this trial is predefined in its `actual_outcome` column.
- `potential_outcome1`, `potential_outcome2`: Potential outcomes of the two options in this trial. If `outcome_randomness` is `"random"`, outcomes in each trial will be this value with given `probability`, or 0 otherwise. Values in this column are also displayed in `explicit` phase.
- `actual_outcome1`, `actual_outcome2`: Values in these columns are the realized outcomes. If `outcome_randomness` is `"random"`, you don't need to specify these values, as actual outcomes will be stochastically determined (according to the `probability` values). If `outcome_randomness` is `"pseudorandom"`, you need to specify the actual outcomes of each option in each trial. Across multiple rows of the conditions file, you can implicitly define the options' outcome probabilities.
- `probability1`, `probability2`: If `outcome_randomness` is `"random"`, these are the probabilities with which outcomes are realized in the trial. In the `explicit` phase they are also used to display reward probabilities of the two options explicitly. If `outcome_randomness` is `"pseudorandom"`, the probabilities do not influence realized outcomes in each trial, but are only used for display in the `explicit` phase.

### Addtional Task Settings

Additional task settings (e.g., timing variables, colors, etc.) can be set in the `settings.py` file. You should not be required to make changes to `task.py`.

### Instructions

Task instructions for the different phases can be defined in `instructions.py`.  
Instructions are implemented as `src.slideshow.SlideShow`, allowing forward and backward navigation. Instruction content can be provided as plain text slides (using `src.slideshow.TextSlide`) or image slides (`src.slideshow.ImageSlide`), or a mix of the two.

### Output

If not specified differently, task data are saved to `data`. In addition to the experimental data, task settings (contained in the `exp_info` dictionary), and PsychoPy's own `.psydat` file are saved for every run.

### Stimulus Images

Stimulus images are made with the [Identicon generator](http://identicon.net/).

## References

- Bavard, S., Rustichini, A., & Palminteri, S. (2021). Two sides of the same coin: Beneficial and detrimental consequences of range adaptation in human reinforcement learning. Science Advances, 7(14), eabe0340. https://doi.org/10.1126/sciadv.abe0340
- Gueguen, M. C. M., Anlló, H., Bonagura, D., Kong, J., Hafezi, S., Palminteri, S., & Konova, A. B. (2024). Recent Opioid Use Impedes Range Adaptation in Reinforcement Learning in Human Addiction. Biological Psychiatry, 95(10), 974–984. https://doi.org/10.1016/j.biopsych.2023.12.005

## Todo

- [ ] Include serial port triggers
- [ ] Allow for counterbalancing of trial_type / block-orders and/or disabling random shuffling
- [ ] Perform thorough check of the task. Is everything on time? Is everything shown properly? Is everything recorded? Does the random stimulus mapping work as expected?
- [ ] Document output file
- [ ] Write script to create `conditions.csv` mirroring literature
- [ ] (low priority) What if we want to skip phases? problems: RNG, points counting.
- [ ] (low priority) Check if we can read the settings.json for a rerun
- [x] Integrate Tobii Eyetracker using [Titta](https://github.com/marcus-nystrom/Titta)
- [x] ~~Clarify: Is feedback ("?") shown if no response given? -> No~~
- [x] ~~(Bug): Explicit phase trials with "pseudorandom" mode do not make any sense, because probabilities are shown, but not used. Shown outcomes are always realized.~~
- [x] ~~Implement actual stochastic outcomes that use `probability` columns of the conditions file~~
- [x] ~~Research casino animation during choice phase: could be done by prerendering a movie for each symbol and showing a movie~~
- [x] ~~Revise feedback phases. "none" becomes "skip". "partial" and "none" need to show question marks.~~
- [x] ~~Make timing physiology compatible: Allow for fixed (choice+feedback) duration. In this case, what happens to missed responses?~~
- [x] ~~see if we can record screen resolution into data or experiment_settings~~
- [x] ~~variable ITIs~~
- [x] ~~debriefing slides should be slides not slideshow~~
- [x] ~~Add support for multiple stimulus sets (e.g., to use for different visits)~~
- [x] ~~Check if trials are randomized within blocks if temporal_arrangemend == 'blocked'~~
- [x] ~~Double check temporal arrangement options. I think there should also be randomization if this is "blocked".~~
- [x] ~~fix bug with random seed. currently, changing it in the GUI doesnt do anything~~
- [x] ~~Fix ImageSlide instructions~~
- [x] ~~End screen message can be SlideShow, too~~
- [x] ~~Remove unnecessary "exp_info" in main script. only necessary within functions~~
- [x] ~~Include intermediate points tally~~
- [x] ~~Ensure all data are recorded~~
- [x] ~~Keep track of rewards over trials (for each phase)~~
- [x] ~~Check if image size is specified properly~~
- [x] ~~Specify text color~~
- [x] ~~Make trials look nicer: Include background and feedback rectangles~~
- [x] ~~Make counterfactual outcome have different color~~
- [x] ~~Implement explicit phase~~
- [x] ~~Record all data (ideally, just include all condition data)~~
- [x] ~~Is feedback an option in the explicit phase?~~
- [x] ~~Refactor code to reduce duplication across phases~~
- [x] ~~Prepare serial port triggers (via `exp_info`?)~~
- [x] ~~Implement ITI~~
- [x] ~~Move timing variables into `exp_info` (currently hardcoded in `trial.run()`)~~
- [x] ~~Implement random assignment of icons to choice options~~
- [x] ~~Implement temporal arrangement (`temporal_arrangement`; "blocked" vs. "interleaved")~~
- [x] ~~Fix instruction slideshow~~
- [x] ~~Implement left/right shuffle (currently called `stim1pos`)~~
