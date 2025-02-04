#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Felix Molter
2025-02-03
felixmolter@gmail.com
"""

from psychopy import visual, event, core, data, gui, sound
from psychopy.tools.filetools import fromFile, toFile
from string import ascii_uppercase

import numpy as np
import pandas as pd
from os.path import join
import os
import json

from src import ImageSlide, TextSlide, SlideShow, Trial

if __name__ == "__main__":
    #########################
    ## Experiment settings ##
    #########################

    ## Experiment
    experiment_name = (
        "Reinforcement-Learning Task"  # Name of the experiment shown in menus
    )
    experiment_label = "rl-context-task"  # Label of the experiment, used in logfiles

    # Messages
    end_screen_message = "Ciao Kakao."

    # Temporal arrangement: Randomize trial order within a block? "blocked" or "interleaved"? (See Bavard et al., 2021, Fig 1)
    temporal_arrangement = "blocked"  # blocked, interleaved; Gueguen used blocked

    ## Stimulus size and position
    text_height = 0.05  # in fraction of display height

    # Timing
    duration_timeout = float(
        "inf"
    )  # timeout duration, None = self paced, used by Bavard & Gueguen
    duration_choice = 0.5  # time for choice to be indicated (black border around chosen symbol; 500 ms used by Bavard)
    duration_outcome = 1.0  # time for the outcome to be shown
    duration_iti = 0.2

    # Visual stim settings
    rect_linewidth = 3
    rect_width = 0.2
    rect_height = 0.2
    pos_left = -0.25
    pos_right = +0.25
    outcome_color = "limegreen"

    # Screen
    screen_size = [1980, 1080]  # ignored, if fullscreen = True, I think
    fullscreen = True
    monitor = "testMonitor"  # name of the monitor configuration used (see PsychoPy monitor settings)

    # Logfile
    logfile_folder = "data"  # folder where to save logfiles
    if not os.path.exists(logfile_folder):
        os.makedirs(logfile_folder)

    # Trials / Conditions
    ## Trial information will be loaded from a separate .csv file
    conditions = pd.read_csv(os.path.join("stim", "conditions.csv"))

    # Responses
    button_quit = "escape"
    button_left = "f"
    button_right = "j"

    # Instruction buttons
    button_instr_next = "right"
    button_instr_previous = "left"
    button_instr_finish = "space"
    button_instr_skip = "s"
    button_instr_quit = button_quit

    # Misc.
    __version__ = 0.1  # because I pretend to know how to make software

    ############################
    ## Experiment setting GUI ##
    ############################
    # Try to read experiment settings from a previous run
    # this does not work on Windows atm
    try:
        exp_info = fromFile("lastRunSettings.pickle")
    # If there is none, then we use a default parameter set
    except:
        exp_info = {
            "Subject": "",
            "Experimenter": "",
            "Session:": "",
        }
    # Add current time
    exp_info["Date"] = data.getDateStr(format="%Y%m%d")
    exp_info["Time"] = data.getDateStr(format="%H%M")

    # Draw a random random seed
    exp_info["random_seed"] = np.random.randint(100, 999)

    # Present the dialog to change parameters:
    dlg = gui.DlgFromDict(exp_info, title=experiment_name, fixed=["Date", "Time"])

    # Set and save random seed
    np.random.seed(exp_info["random_seed"])

    if dlg.OK:
        toFile("lastRunSettings.pickle", exp_info)
    else:
        core.quit()

    # Make random mapping of symbol IDs (ABCDEFGH and training ones) to images (1,2,3,4,5.png)
    n_symbols_training = 4  # ideally read this from the conditions
    n_symbols_task = 8  # ideally read this from the conditions
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
    exp_info["logfile_path"] = logfile_path

    # Save all experiment settings
    exp_info["end_screen_message"] = end_screen_message
    exp_info["duration_timeout"] = duration_timeout
    exp_info["duration_choice"] = duration_choice
    exp_info["duration_outcome"] = duration_outcome
    exp_info["duration_iti"] = duration_iti
    exp_info["temporal_arrangement"] = temporal_arrangement
    exp_info["outcome_color"] = outcome_color
    exp_info["text_height"] = text_height
    exp_info["rect_linewidth"] = rect_linewidth
    exp_info["rect_width"] = rect_width
    exp_info["rect_height"] = rect_height
    exp_info["pos_left"] = pos_left
    exp_info["pos_right"] = pos_right
    exp_info["buttons"] = dict(
        button_quit=button_quit,
        button_left=button_left,
        button_right=button_right,
    )
    exp_info["stimuli"] = dict(conditions=conditions.to_dict())
    exp_info["stimulus_map"] = dict(task_symbol_map, **training_symbol_map)

    # Save experiment settings for this run
    with open(f"{logfile_path}_settings.json", "w") as file:
        json.dump(exp_info, file)

    # Set up experiment object
    exp = data.ExperimentHandler(
        name=experiment_name, version=__version__, dataFileName=logfile_path
    )

    ###############################
    ## Set up window and stimuli ##
    ###############################

    # Set up the experiment window
    win = visual.Window(
        size=screen_size, monitor=monitor, fullscr=fullscreen, units="height"
    )
    win.mouseVisible = False

    # Set up stimuli

    # Stimulus Images
    image_left = visual.ImageStim(
        win, image=join("stim", "images", "t1.png"), pos=(pos_left, 0)
    )
    image_right = visual.ImageStim(
        win, image=join("stim", "images", "t2.png"), pos=(pos_right, 0)
    )
    images = [image_left, image_right]

    ## Set up feedback rectangles
    rect_left = visual.Rect(
        win,
        pos=[pos_left, 0],
        size=[rect_width, rect_height],
        lineWidth=rect_linewidth,
        lineColor="black",
        units="height",
    )
    rect_right = visual.Rect(
        win,
        pos=[pos_right, 0],
        size=[rect_width, rect_height],
        lineWidth=rect_linewidth,
        lineColor="black",
        units="height",
    )
    rects = [rect_left, rect_right]

    # Outcomes
    outcome_left = visual.TextStim(
        win, text="", pos=(pos_left, 0), height=text_height, color=outcome_color
    )
    outcome_right = visual.TextStim(
        win, text="", pos=(pos_right, 0), height=text_height, color=outcome_color
    )
    outcomes = [outcome_left, outcome_right]

    # save all pre-made visual elements
    visual_elements = dict(images=images, rects=rects, outcomes=outcomes)

    ######################
    ## Start experiment ##
    ######################

    # Display instructions
    ## Load instruction images
    n_slides = 3
    training_instr_slides = [
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
        )
        for i in range(n_slides)
    ]

    ## Run instruction slideshow
    ## button to start task
    start_button = "space"
    instruction = SlideShow(
        win=win,
        slides=training_instr_slides,
        keys_finish=[button_instr_finish],
        keys_previous=[button_instr_previous],
        keys_next=[button_instr_next],
        keys_quit=[button_quit],
        keys_skip=[button_instr_skip],
    )
    response = instruction.run()

    # -------------- #
    # Training phase #
    # -------------- #
    conditions_training = conditions.loc[conditions["phase"] == "training"]
    ## button to repeat training
    repeat_button = "r"
    ## button to proceed
    start_button = "space"

    n_repeats_max = 2  # TODO: move this up
    n_repeats = 0
    repeat_training = True
    while repeat_training and n_repeats <= n_repeats_max:
        for idx, trial_info in conditions_training.iterrows():
            print(trial_info)

            trial = Trial(
                trial_info=trial_info,
                exp=exp,
                exp_info=exp_info,
                win=win,
                visual_elements=visual_elements,
            )
            trial.prepare()
            trial.run()
            trial.log()

        response = SlideShow(
            win=win,
            slides=[
                TextSlide(
                    win=win,
                    text=f"Mit '{repeat_button.capitalize()}' Training wiederholen\n\noder\n\nMit '{start_button.capitalize()}' fortfahren.",
                    height=text_height,
                ),
            ],
            keys_finish=[start_button, repeat_button],
        ).run()
        if not repeat_button in response:
            repeat_training = False
        else:
            n_repeats += 1
            if n_repeats > n_repeats_max:
                response = SlideShow(
                    win=win,
                    slides=[
                        TextSlide(
                            win=win,
                            text=f"Sie haben bereits die maximale Anzahl an Wiederholungen der Übungsrunde erreicht.\n\nMit '{start_button.capitalize()}' beginnen.",
                            height=text_height,
                        ),
                    ],
                    keys_finish=[start_button],
                ).run()

    # -------------- #
    # Learning phase #
    # -------------- #
    conditions_learning = conditions.loc[conditions["phase"] == "learning"]
    if len(conditions_learning) > 0:

        # Show learning phase instructions
        n_slides = 3
        learning_instr_slides = [
            TextSlide(
                win=win,
                text=(
                    f"Instructions: Learning Phase\n"
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
            )
            for i in range(n_slides)
        ]

        ## Run instruction slideshow
        ## button to start task
        start_button = "space"
        instruction = SlideShow(
            win=win,
            slides=learning_instr_slides,
            keys_finish=[button_instr_finish],
            keys_previous=[button_instr_previous],
            keys_next=[button_instr_next],
            keys_quit=[button_quit],
            keys_skip=[button_instr_skip],
        )
        response = instruction.run()

        blocks = conditions_learning["block"].unique()
        n_blocks = len(blocks)
        for b, block in enumerate(blocks):
            # Show a block divider if there are multiple blocks
            if n_blocks > 1:
                SlideShow(
                    win=win,
                    slides=[
                        TextSlide(
                            win=win,
                            text=f"Block {b + 1} von {len(blocks)}\n\nMit '{start_button}' beginnen",
                            height=text_height,
                        ),
                    ],
                    keys_finish=[start_button],
                ).run()

            trials_block = conditions_learning.loc[
                conditions_learning["block"] == block
            ]
            if temporal_arrangement == "interleaved":
                trials_block = trials_block.sample(frac=1)
            for idx, trial_info in trials_block.iterrows():
                print(trial_info)

                trial = Trial(
                    trial_info=trial_info,
                    exp=exp,
                    exp_info=exp_info,
                    win=win,
                    visual_elements=visual_elements,
                )
                trial.prepare()
                trial.run()
                trial.log()

    # -------------- #
    # Transfer phase #
    # -------------- #
    conditions_transfer = conditions.loc[conditions["phase"] == "transfer"]
    if len(conditions_transfer) > 0:

        # Show transfer phase instructions
        n_slides = 3
        transfer_instr_slides = [
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
            )
            for i in range(n_slides)
        ]

        ## Run instruction slideshow
        ## button to start task
        start_button = "space"
        instruction = SlideShow(
            win=win,
            slides=transfer_instr_slides,
            keys_finish=[button_instr_finish],
            keys_previous=[button_instr_previous],
            keys_next=[button_instr_next],
            keys_quit=[button_quit],
            keys_skip=[button_instr_skip],
        )
        response = instruction.run()

        # Run transfer phase
        blocks = conditions_transfer["block"].unique()
        n_blocks = len(blocks)
        for b, block in enumerate(blocks):
            # Show a block divider if there are multiple blocks
            if n_blocks > 1:
                SlideShow(
                    win=win,
                    slides=[
                        TextSlide(
                            win=win,
                            text=f"Block {b + 1} von {len(blocks)}\n\nMit '{start_button}' beginnen",
                            height=text_height,
                        ),
                    ],
                    keys_finish=[start_button],
                ).run()

            trials_block = conditions_transfer.loc[
                conditions_transfer["block"] == block
            ]
            if temporal_arrangement == "interleaved":
                trials_block = trials_block.sample(frac=1)
            for idx, trial_info in trials_block.iterrows():
                print(trial_info)

                trial = Trial(
                    trial_info=trial_info,
                    exp=exp,
                    exp_info=exp_info,
                    win=win,
                    visual_elements=visual_elements,
                )
                trial.prepare()
                trial.run()
                trial.log()

    # -------------- #
    # Explicit phase #
    # -------------- #
    print("Explicit phase")
    visual.TextStim(
        win,
        f"Explicit phase is work in progress. Continue with '{button_instr_finish}'.",
        height=text_height,
    )
    end_screen.draw()
    win.flip()

    ## Wait for keypress
    event.waitKeys(keyList=[button_instr_finish])

    # ------------------------------ #
    # End of experiment / Debriefing #
    # ------------------------------ #
    # Show end screen
    end_screen = visual.TextStim(
        win,
        end_screen_message + f"\n\n'{button_quit.capitalize()}' to quit.",
        height=text_height,
    )
    end_screen.draw()
    win.flip()

    ## Wait for keypress
    event.waitKeys(keyList=[button_quit])

    # Finish the experiment
    core.quit()
