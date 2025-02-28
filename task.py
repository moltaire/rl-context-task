#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Two-Armed-Bandit Reinforcement-Learning-Task
with training, learning, transfer, and explicit phases,
and options to control feedback information.
Modelled after Bavard et al. (2021) and Gueguen et al. (2024)

For documentation beyond this file, see:
https://github.com/moltaire/rl-context-task

References:
- Bavard, S., Rustichini, A., & Palminteri, S. (2021). Two sides of the same coin: Beneficial and detrimental consequences of range adaptation in human reinforcement learning. Science Advances, 7(14), eabe0340. https://doi.org/10.1126/sciadv.abe0340
- Gueguen, M. C. M., Anlló, H., Bonagura, D., Kong, J., Hafezi, S., Palminteri, S., & Konova, A. B. (2024). Recent Opioid Use Impedes Range Adaptation in Reinforcement Learning in Human Addiction. Biological Psychiatry, 95(10), 974–984. https://doi.org/10.1016/j.biopsych.2023.12.005

Felix Molter
2025-02-03
felixmolter@gmail.com
"""
import psychopy

psychopy.useVersion("2024.1.0")

from psychopy import visual, event, core, data, gui, sound
from psychopy.tools.filetools import fromFile, toFile
from string import ascii_uppercase

import numpy as np
import pandas as pd
import random
from os.path import join
import os
import json

from src import ImageSlide, TextSlide, SlideShow, Trial

__version__ = 0.1  # because I pretend to know how to make software

if __name__ == "__main__":

    # Load settings from external settings.py file
    from settings import *

    ## Load conditions file
    conditions = pd.read_csv(os.path.join("stim", conditions_file))

    ## Create folder if it does not exist
    if not os.path.exists(logfile_folder):
        os.makedirs(logfile_folder)

    # PLACEHOLDER FOR SERIAL PORT SETUP # # # # # #
    if use_serialport:
        # TODO: Include this. # # # # # # # # # # # # #
        serialport = None
    else:
        serialport = None

    # PLACEHOLDER FOR EYE-TRACKER SETUP # # # # # #
    if use_eyetracker:
        # TODO: Include this. # # # # # # # # # # # # #
        eyetracker = None
    else:
        eyetracker = None

    ##############################
    # ===== Experiment GUI ===== #
    ##############################
    # This configures the little
    # dialogue box to enter infos.
    # You should not be required
    # to make changes here.

    # Try to read experiment settings from a previous run
    try:
        exp_info = fromFile("lastRunSettings.pickle")
        exp_info["Stimulus-Set"] = ["Set 1", "Set 2"]
    # If there is none, then we use a default parameter set
    except:
        exp_info = {
            "Subject": "",
            "Experimenter": "",
            "Session": "",
            "Stimulus-Set": ["Set 1", "Set 2"],
        }
    # Add current time
    exp_info["Date"] = data.getDateStr(format="%Y%m%d")
    exp_info["Time"] = data.getDateStr(format="%H%M")

    # Draw a random random seed
    random_seed = np.random.randint(100, 999)
    exp_info["random_seed"] = random_seed

    # Present the dialog to change parameters:
    dlg = gui.DlgFromDict(exp_info, title=experiment_name, fixed=["Date", "Time"])

    # Set and save random seed
    np.random.seed(exp_info["random_seed"])

    if dlg.OK:
        toFile("lastRunSettings.pickle", exp_info)
    else:
        core.quit()

    ############################
    # ===== Window setup ===== #
    ############################

    win = visual.Window(
        size=screen_size,
        monitor=monitor,
        fullscr=fullscreen,
        units="height",
        color=background_color,
    )
    win.mouseVisible = False

    if fullscreen:
        screen_size = win.monitor.getSizePix()

    ############################
    # ===== Instructions ===== #
    ############################
    # Adapt to your preference!

    ## Training phase
    n_slides = 3
    instr_slides_training = [
        TextSlide(
            win=win,
            text=(
                f"Instructions: Training Phase\n"
                + f"Slide {i + 1}/{n_slides} text.\n\n"
                + f"({button_instr_previous.capitalize()}) Previous - "
                + f"({button_instr_next.capitalize()}) Next - "
                + f"({button_instr_skip.capitalize()}) Skip"
                + (
                    f" - ({button_instr_finish.capitalize()}) Continue with task"
                    if i == (n_slides - 1)
                    else ""
                )
            ),
            height=text_height,
            color=text_color,
        )
        for i in range(n_slides)
    ]

    ## Learning phase
    ### Using image slides for illustration here
    instr_slides_learning = [
        ImageSlide(
            win=win,
            image=join(
                "instructions",
                "learning-phase",
                f"rl-context-task_instructions_learning-phase.{i:03d}.png",
            ),
        )
        for i in [1, 2, 3]
    ]

    ## Transfer phase
    n_slides = 3
    instr_slides_transfer = [
        TextSlide(
            win=win,
            text=(
                f"Instructions: Transfer Phase\n"
                + f"Slide {i + 1}/{n_slides} text. No more feedback!\n\n"
                + f"({button_instr_previous.capitalize()}) Previous - "
                + f"({button_instr_next.capitalize()}) Next - "
                + f"({button_instr_skip.capitalize()}) Skip"
                + (
                    f" - ({button_instr_finish.capitalize()}) Continue with task"
                    if i == (n_slides - 1)
                    else ""
                )
            ),
            height=text_height,
            color=text_color,
        )
        for i in range(n_slides)
    ]

    ## Explicit phase
    n_slides = 3
    instr_slides_explicit = [
        TextSlide(
            win=win,
            text=(
                f"Instructions: Explicit Phase\n"
                + f"Slide {i + 1}/{n_slides} text. No more symbols, but numbers!\n\n"
                + f"({button_instr_previous.capitalize()}) Previous - "
                + f"({button_instr_next.capitalize()}) Next - "
                + f"({button_instr_skip.capitalize()}) Skip"
                + (
                    f" - ({button_instr_finish.capitalize()}) Continue with task"
                    if i == (n_slides - 1)
                    else ""
                )
            ),
            height=text_height,
            color=text_color,
        )
        for i in range(n_slides)
    ]

    ## Debriefing
    debriefing_slides = [
        TextSlide(
            win=win,
            text=(
                f"Debriefing\n\n"
                + f"Ciao Kakao!\n"
                + f"Mit '{button_instr_finish.capitalize()}' beenden Sie das Experiment."
            ),
            height=text_height,
            color=text_color,
        )
    ]

    #########################################################################################################
    ## FROM THIS POINT ON, THERE BE DRAGONS. ONLY GO THERE IF YOU KNOW WHAT YOU'RE DOING AND HAVE A BACKUP ##
    #########################################################################################################

    # Make random mapping of symbol IDs (ABCDEFGH and training ones) to images (1,2,3,4,5.png)
    ## Get the number of symbols needed
    ## After a random number generator seed has been set, there will be a
    ## participant-specific mapping of symbols (e.g., 1.png) to IDs (e.g., A)
    ## Don't change unless you're really sure about it.
    n_symbols_training = np.unique(
        conditions.query("phase == 'training'")[["symbol1", "symbol2"]].values.ravel()
    ).size
    n_symbols_task = np.unique(
        conditions.query("phase == 'learning'")[["symbol1", "symbol2"]].values.ravel()
    ).size
    print(
        f"Assuming {n_symbols_training} training symbols and {n_symbols_task} task symbols."
    )

    symbol_ids = ascii_uppercase[:n_symbols_task]
    image_names = [f"{i + 1}.png" for i in range(n_symbols_task + n_symbols_training)]
    np.random.shuffle(image_names)  # shuffle in place

    # first n_symbols_training images are for training
    training_symbol_map = {
        f"T{i + 1}": image_names[i] for i in range(n_symbols_training)
    }
    # next n_symbols_task images are for main task
    task_symbol_map = {
        symbol_id: image_names[n_symbols_training + i]
        for i, symbol_id in enumerate(symbol_ids)
    }

    # Build the logfile name
    logfile_name = f"task-{experiment_label}_subject-{exp_info['Subject']}_date-{exp_info['Date']}_time-{exp_info['Time']}"
    logfile_path = os.path.join(logfile_folder, logfile_name)

    # Save all other experiment settings
    ## Duration
    exp_info["duration_timeout"] = duration_timeout
    exp_info["duration_choice"] = duration_choice
    exp_info["duration_outcome"] = duration_outcome
    exp_info["duration_iti"] = duration_iti
    exp_info["duration_iti_jitter"] = duration_iti_jitter
    exp_info["duration_fixed_response"] = duration_fixed_response
    exp_info["duration_first_trial_blank"] = duration_first_trial_blank

    ## Visuals
    exp_info["background_color"] = background_color
    exp_info["text_color"] = text_color
    exp_info["outcome_color"] = outcome_color
    exp_info["outcome_color_counterfactual"] = outcome_color_counterfactual
    exp_info["outcome_text_scale"] = outcome_text_scale
    exp_info["text_height"] = text_height
    exp_info["rect_linewidth"] = rect_linewidth
    exp_info["rect_width"] = rect_width
    exp_info["rect_height"] = rect_height
    exp_info["pos_left"] = pos_left
    exp_info["pos_right"] = pos_right
    exp_info["screen_size"] = screen_size
    exp_info["animation_speed"] = animation_speed

    ## Experiment Flow
    exp_info["temporal_arrangement"] = temporal_arrangement
    exp_info["buttons"] = dict(
        button_quit=button_quit,
        button_left=button_left,
        button_right=button_right,
        button_instr_next=button_instr_next,
        button_instr_previous=button_instr_previous,
        button_instr_finish=button_instr_finish,
        button_instr_skip=button_instr_skip,
        button_instr_quit=button_instr_quit,
        button_instr_repeat=button_instr_repeat,
    )
    exp_info["training_n_repeats_max"] = training_n_repeats_max
    exp_info["show_block_dividers"] = show_block_dividers
    exp_info["show_score_after_phase"] = show_score_after_phase
    exp_info["total_reward"] = 0  # used to track reward
    exp_info["logfile_path"] = logfile_path

    ## Stimuli
    exp_info["stimuli"] = dict(conditions=conditions.to_dict())
    exp_info["stimulus_map"] = dict(
        task_symbol_map, **training_symbol_map
    )  # combines task- and training symbol map

    ## External Hardware
    exp_info["use_eyetracker"] = use_eyetracker
    exp_info["use_serialport"] = use_serialport

    # Save experiment settings for this run
    with open(f"{logfile_path}_settings.json", "w") as file:
        json.dump(exp_info, file)

    # Also add serial port (after .json dump)
    exp_info["serialport"] = serialport

    # Add eye tracking object
    exp_info["eyetracker"] = eyetracker

    # Set up experiment object
    exp = data.ExperimentHandler(
        name=experiment_name, version=__version__, dataFileName=logfile_path
    )

    ###########################
    ## Set up visual stimuli ##
    ###########################

    # Set up stimuli
    ## Stimulus Images
    ## Image files are just placeholder, will be replaced in `trial.prepare()`
    image_left = visual.ImageStim(
        win,
        image=join("stim", "images", str(exp_info["Stimulus-Set"]), "1.png"),
        pos=(pos_left, 0),
        size=(symbol_width, symbol_height),
    )
    image_right = visual.ImageStim(
        win,
        image=join("stim", "images", str(exp_info["Stimulus-Set"]), "2.png"),
        pos=(pos_right, 0),
        size=(symbol_width, symbol_height),
    )
    images = [image_left, image_right]

    ## Videos
    ## Files are just placeholder, will be replaced in `trial.prepare()`
    video_left = visual.MovieStim(
        win,
        filename="",  # join("stim", "images", str(exp_info["Stimulus-Set"]), "anim", "1.mp4"),
        pos=(pos_left, 0),
        size=(symbol_width, symbol_height),
        loop=False,
        autoStart=False,
        units="height",
    )
    video_right = visual.MovieStim(
        win,
        filename="",  # join("stim", "images", str(exp_info["Stimulus-Set"]), "anim", "2.mp4"),
        pos=(pos_right, 0),
        size=(symbol_width, symbol_height),
        loop=False,
        autoStart=False,
        units="height",
    )
    videos = [video_left, video_right]

    ## Set up background rectangles
    bg_rect_left = visual.Rect(
        win,
        pos=[pos_left, 0],
        size=[rect_width, rect_height],
        lineWidth=rect_linewidth,
        lineColor=rect_linecolor,
        fillColor=rect_background_color,
        units="height",
    )
    bg_rect_right = visual.Rect(
        win,
        pos=[pos_right, 0],
        size=[rect_width, rect_height],
        lineWidth=rect_linewidth,
        lineColor=rect_linecolor,
        fillColor=rect_background_color,
        units="height",
    )
    bg_rects = [bg_rect_left, bg_rect_right]

    ## Set up feedback rectangles
    fb_rect_left = visual.Rect(
        win,
        pos=[pos_left, 0],
        size=[rect_width, rect_height],
        lineWidth=fb_rect_linewidth,
        lineColor=fb_rect_linecolor,
        units="height",
    )
    fb_rect_right = visual.Rect(
        win,
        pos=[pos_right, 0],
        size=[rect_width, rect_height],
        lineWidth=fb_rect_linewidth,
        lineColor=fb_rect_linecolor,
        units="height",
    )
    fb_rects = [fb_rect_left, fb_rect_right]

    ## Outcomes
    outcome_left = visual.TextStim(
        win,
        text="",
        pos=(pos_left, 0),
        height=text_height * outcome_text_scale,
        color=outcome_color,
    )
    outcome_right = visual.TextStim(
        win,
        text="",
        pos=(pos_right, 0),
        height=text_height * outcome_text_scale,
        color=outcome_color,
    )
    outcomes = [outcome_left, outcome_right]

    ## Explicit phase TextStims
    explicit_left = visual.TextStim(
        win,
        text="",
        pos=(pos_left, 0),
        height=text_height,
        color=text_color,
    )
    explicit_right = visual.TextStim(
        win,
        text="",
        pos=(pos_right, 0),
        height=text_height,
        color=text_color,
    )
    explicit = [explicit_left, explicit_right]

    # Save all pre-made visual elements
    visual_elements = dict(
        images=images,
        videos=videos,
        bg_rects=bg_rects,
        outcomes=outcomes,
        explicit=explicit,
        fb_rects=fb_rects,
    )
    ## They are saved to `exp_info` so that `run_phase` and `Trial.run()` can use them
    exp_info["visual_elements"] = visual_elements

    ######################
    ## Start experiment ##
    ######################

    def run_phase(phase, conditions, instruction_slides, exp_info, exp, win):
        """
        This function runs a single phase of the task.

        Specifically, it
        - selects the conditions for this phase
        - shows instructions
        - runs trials (with optional block dividers)
        - optionally shows points tally after phase is done

        Args:
            phase (str): "training", "learning", "transfer", or "explicit"
            conditions (pandas.DataFrame): _description_
            instructions (slideshow.Slide): list of slide objects
            exp_info (_type_): _description_
        """
        ## Extract conditions
        conditions_phase = conditions.loc[conditions["phase"] == phase]

        # Only proceed if there are conditions to do
        if len(conditions_phase) > 0:
            print(f"Running {len(conditions_phase)} trials of '{phase}' phase.")

            ## Run instruction slideshow
            instruction = SlideShow(
                win=win,
                slides=instruction_slides,
                keys_finish=[exp_info["buttons"]["button_instr_finish"]],
                keys_previous=[exp_info["buttons"]["button_instr_previous"]],
                keys_next=[exp_info["buttons"]["button_instr_next"]],
                keys_quit=[exp_info["buttons"]["button_quit"]],
                keys_skip=[exp_info["buttons"]["button_instr_skip"]],
            )
            response = instruction.run()
            # Blank screen after instructions
            win.flip()
            core.wait(exp_info["duration_first_trial_blank"])

            ## Iterate over blocks
            blocks = conditions_phase["block"].unique()
            n_blocks = len(blocks)
            for b, block in enumerate(blocks):
                if exp_info["show_block_dividers"]:
                    # Show a block divider if there are multiple blocks
                    if n_blocks > 1:
                        SlideShow(
                            win=win,
                            slides=[
                                TextSlide(
                                    win=win,
                                    text=f"Block {b + 1} von {len(blocks)}\n\nMit '{exp_info['buttons']['button_instr_finish'].capitalize()}' beginnen",
                                    height=exp_info["text_height"],
                                    color=exp_info["text_color"],
                                ),
                            ],
                            keys_finish=[exp_info["buttons"]["button_instr_finish"]],
                        ).run()
                        # Blank screen after block message
                        win.flip()
                        core.wait(exp_info["duration_first_trial_blank"])

                trials_block = conditions_phase.loc[conditions_phase["block"] == block]

                # Temporal arrangement: Blocked or interleaved
                ## "interleaved" randomly shuffles all trials in this block
                if exp_info["temporal_arrangement"] == "interleaved":
                    trials_block = trials_block.sample(frac=1)
                ## "blocked" will keep trials of the same `trial_type` in this block together,
                ## but randomize the order of these trial_type chunks
                elif exp_info["temporal_arrangement"] == "blocked":
                    # split by trial_type
                    chunks = [
                        trials_of_type.sample(frac=1)  # randomize within each chunk
                        for _, trials_of_type in trials_block.groupby("trial_type")
                    ]
                    # shuffle chunks
                    random.shuffle(chunks)
                    # concatenate them
                    trials_block = pd.concat(chunks).reset_index(drop=True)
                else:
                    raise ValueError(
                        f"`temporal_arrangement` must be in ['interleaved', 'blocked], but is '{exp_info['temporal_arrangement']}'."
                    )

                # Iterate through trials of this block
                for idx, trial_info in trials_block.iterrows():
                    print(trial_info)
                    trial = Trial(
                        trial_info=trial_info,
                        exp=exp,
                        exp_info=exp_info,
                        win=win,
                        visual_elements=exp_info["visual_elements"],
                    )
                    trial.prepare()
                    trial.run()
                    trial.log()

        # (optional) show score after phase (not after training, though)
        if phase != "training":
            if exp_info["show_score_after_phase"]:
                SlideShow(
                    win=win,
                    slides=[
                        TextSlide(
                            win=win,
                            text=f"Bisher haben Sie {exp_info['total_reward']:.0f} Punkte gesammelt!"
                            + f"\n\nMit '{exp_info['buttons']['button_instr_finish'].capitalize()}' fortfahren.",
                            height=exp_info["text_height"],
                            color=exp_info["text_color"],
                        ),
                    ],
                    keys_finish=[exp_info["buttons"]["button_instr_finish"]],
                ).run()

        else:  # No conditions to show
            print(f"No conditions with phase '{phase}' in `conditions`.")
            return

    # -------------- #
    # Training phase #
    # -------------- #
    # This phase has a bit more code than the others to allow for it to be repeated.

    n_repeats = 0
    repeat_training = True  # set to False to skip training
    while repeat_training and n_repeats <= training_n_repeats_max:
        run_phase(
            phase="training",
            conditions=conditions,
            instruction_slides=instr_slides_training,
            exp_info=exp_info,
            exp=exp,
            win=win,
        )
        # check if maximum repeats is reached
        if n_repeats == training_n_repeats_max:
            response = SlideShow(
                win=win,
                slides=[
                    TextSlide(
                        win=win,
                        text=f"Sie haben die maximale Anzahl an Wiederholungen der Übungsrunde erreicht.\n\nMit "
                        + f"'{button_instr_finish.capitalize()}' fortfahren.",
                        height=text_height,
                        color=text_color,
                    ),
                ],
                keys_finish=[button_instr_finish],
            ).run()
            repeat_training = False
        else:  # otherwise show training repetition dialogue
            response = SlideShow(
                win=win,
                slides=[
                    TextSlide(
                        win=win,
                        text=f"Mit '{button_instr_repeat.capitalize()}' Training wiederholen\n\n"
                        + f"oder\n\nmit '{button_instr_finish.capitalize()}' fortfahren.",
                        height=text_height,
                        color=text_color,
                    ),
                ],
                keys_finish=[
                    button_instr_finish,
                    button_instr_repeat,
                ],
            ).run()
            if not button_instr_repeat in response:
                repeat_training = False
            else:
                n_repeats += 1

    # -------------- #
    # Learning phase #
    # -------------- #
    run_phase(
        phase="learning",
        conditions=conditions,
        instruction_slides=instr_slides_learning,
        exp_info=exp_info,
        exp=exp,
        win=win,
    )

    # -------------- #
    # Transfer phase #
    # -------------- #
    run_phase(
        phase="transfer",
        conditions=conditions,
        instruction_slides=instr_slides_transfer,
        exp_info=exp_info,
        exp=exp,
        win=win,
    )

    # -------------- #
    # Explicit phase #
    # -------------- #
    run_phase(
        phase="explicit",
        conditions=conditions,
        instruction_slides=instr_slides_explicit,
        exp_info=exp_info,
        exp=exp,
        win=win,
    )

    # ------------------------------ #
    # End of experiment / Debriefing #
    # ------------------------------ #
    SlideShow(
        win=win,
        slides=debriefing_slides,
        keys_finish=[button_instr_finish],
        keys_previous=[button_instr_previous],
        keys_next=[button_instr_next],
        keys_quit=[button_quit],
        keys_skip=[button_instr_skip],
    ).run()

    # Print total points earned to console
    total_score_string = f"$$$ Total points earned: {exp_info['total_reward']} Pts. $$$"
    print(len(total_score_string) * "$")
    print(total_score_string)
    print(len(total_score_string) * "$")

    # Finish the experiment
    core.quit()
