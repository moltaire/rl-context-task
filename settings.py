###################################
# ===== Experiment Settings ===== #
###################################
# Change variables to customize the
# task. Possible variable values are
# described in comments.

## Experiment
experiment_name = (
    "Reinforcement-Learning Task"  # Name of the experiment shown in menus
)
experiment_label = "rl-context-task"  # Label of the experiment, used in logfiles

# General experiment flow and settings
## Temporal arrangement: Randomize trial order within a block? "blocked" or "interleaved"? (See Bavard et al., 2021, Fig 1)
temporal_arrangement = "blocked"  # ["blocked", "interleaved"]; Gueguen used "blocked", Bavard et al., (2021) tried both.

## Training settings
training_n_repeats_max = 2  # Maximum number of training repetitions

## Show block dividers
show_block_dividers = False  # [True, False]

## Show score between rounds
show_score_after_phase = True  # [True, False]

# Trials / Conditions
## Trial information will be loaded from a separate .csv file
conditions_file = "conditions.csv"

# Buttons
## (any keyboard button code will do for these)
## Responses
button_left = "f"
button_right = "j"

## Quit button (don't tell participants)
button_quit = "q"

## Instruction buttons (to move around in instructions)
button_instr_next = "right"  # move to next slide
button_instr_previous = "left"  # move to previous slide
button_instr_finish = "space"  # continues after
button_instr_skip = "s"  # moves to last slide
button_instr_repeat = "r"  # to repeat training (and instructions)
button_instr_quit = button_quit  # quit experiment

# Timing
## Timing variables are provided in seconds
duration_timeout = 5.0  # float("inf")  # timeout duration, float("inf") = self paced, used by Bavard & Gueguen
duration_choice = 0.5  # time for choice to be indicated (black border around chosen symbol; 500 ms used by Bavard)
duration_outcome = 1.0  # time for the outcome to be shown (seconds)
duration_iti = 0.2  # inter trial interval (seconds)
duration_iti_jitter = 0  # random jitter around `duration_iti`. ITIs will be distributed normally between duration_iti ± iti_jitter / 2
duration_first_trial_blank = 1  # a blank screen after instructions, before the first trial of each block phase

## This next setting can be used to fix the total time used for the two phases
## - `response` (participant deliberates) and
## - `choice` (participant has chosen and their chosen option is highlighted)
## Effectively, if `duration_fixed_response` = True,
## it fills the remainer of `duration_timeout` with the `choice` phase.
## This might be useful for studies using physiological measures that need
## constant trial duration and stimulus events decoupled from response times.
## Note, that this cannot work with `duration_timeout` set to infinity.
duration_fixed_response = False  # [True, False]
if duration_fixed_response:
    assert duration_timeout != float(
        "inf"
    ), "If using `duration_fixed_response`, you must use a finite `duration_timeout`."

# Visual stim settings
## General background and text
background_color = "lightgray"  # named colors or RGB triplets (e.g., (1, 0, 0))
text_color = "black"
text_height = 0.05  # in fraction of display height

## Stimulus positions (left right, units in screen height)
pos_left = -0.25
pos_right = +0.25

## Symbol size (units screen height)
symbol_width = 0.24
symbol_height = 0.24

## Outcome text
outcome_color = "forestgreen"
outcome_color_counterfactual = "gray"
outcome_text_scale = (
    2  # how much bigger should the outcomes be than the other text?
)

## Background rectangle
rect_linewidth = 3  # I think this is pixels?
rect_width = 0.25  # monitor height units
rect_height = 0.25  # monitor height units
rect_linecolor = "black"
rect_background_color = "white"

## Feedback rectangle
fb_rect_linewidth = 12
fb_rect_linecolor = "black"

## Animation
animation_speed = 0.5  # speed of the flicker, 0 is no animation, I think :)

# Screen
fullscreen = True
screen_size = [1280, 1080]  # ignored, if fullscreen = True, I think
monitor = "testMonitor"  # name of the monitor configuration used (see PsychoPy monitor settings)

# Logfile
logfile_folder = "data"  # folder where to save logfiles

# External Hardware
use_eyetracker = False
use_serialport = False