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

    # Training settings
    training_n_repeats_max = 2  # Maximum number of training repetitions

    # Show block dividers
    show_block_dividers = False

    # Show score between rounds
    show_score_after_phase = True

    # Timing
    duration_timeout = float(
        "inf"
    )  # timeout duration, None = self paced, used by Bavard & Gueguen
    duration_choice = 0.5  # time for choice to be indicated (black border around chosen symbol; 500 ms used by Bavard)
    duration_outcome = 1.0  # time for the outcome to be shown
    duration_iti = 0.2

    # Visual stim settings
    rect_linewidth = 3
    rect_width = 0.25
    rect_height = 0.25
    pos_left = -0.25
    pos_right = +0.25
    text_height = 0.05  # in fraction of display height
    background_color = "lightgray"
    text_color = "black"
    outcome_color = "forestgreen"
    outcome_color_counterfactual = "gray"
    rect_linecolor = "black"
    rect_background_color = "white"
    symbol_width = 0.24
    symbol_height = 0.24

    ## Feedback rectangle
    fb_rect_linewidth = 6
    fb_rect_linecolor = "black"

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
    button_instr_repeat = "r"  # to repeat training (and instructions)
    button_instr_quit = button_quit

    # PLACEHOLDER FOR SERIAL PORT SETUP # # # # # #
    serial_port = None  # e.g., None if not in use
    # TODO: Include this. # # # # # # # # # # # # #

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
    exp_info["background_color"] = background_color
    exp_info["text_color"] = text_color
    exp_info["outcome_color"] = outcome_color
    exp_info["outcome_color_counterfactual"] = outcome_color_counterfactual
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
        button_instr_next=button_instr_next,
        button_instr_previous=button_instr_previous,
        button_instr_finish=button_instr_finish,
        button_instr_skip=button_instr_skip,
        button_instr_quit=button_instr_quit,
        button_instr_repeat=button_instr_repeat,
    )
    exp_info["stimuli"] = dict(conditions=conditions.to_dict())
    exp_info["stimulus_map"] = dict(task_symbol_map, **training_symbol_map)
    exp_info["training_n_repeats_max"] = training_n_repeats_max
    exp_info["show_block_dividers"] = show_block_dividers
    exp_info["show_score_after_phase"] = show_score_after_phase
    exp_info["total_reward"] = 0  # used to track reward

    # Save experiment settings for this run
    with open(f"{logfile_path}_settings.json", "w") as file:
        json.dump(exp_info, file)

    # Also add serial port (after .json dump)
    exp_info["serial_port"] = serial_port

    # Set up experiment object
    exp = data.ExperimentHandler(
        name=experiment_name, version=__version__, dataFileName=logfile_path
    )

    ###############################
    ## Set up window and stimuli ##
    ###############################

    # Set up the experiment window
    win = visual.Window(
        size=screen_size,
        monitor=monitor,
        fullscr=fullscreen,
        units="height",
        color=exp_info["background_color"],
    )
    win.mouseVisible = False

    # Set up stimuli
    ## Stimulus Images
    ## Image files are just placeholder, will be replaced in `trial.prepare()`
    image_left = visual.ImageStim(
        win,
        image=join("stim", "images", "1.png"),
        pos=(pos_left, 0),
        size=(symbol_width, symbol_height),
    )
    image_right = visual.ImageStim(
        win,
        image=join("stim", "images", "2.png"),
        pos=(pos_right, 0),
        size=(symbol_width, symbol_height),
    )
    images = [image_left, image_right]

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

    # Outcomes
    outcome_left = visual.TextStim(
        win,
        text="",
        pos=(pos_left, 0),
        height=text_height,
        color=outcome_color,
    )
    outcome_right = visual.TextStim(
        win,
        text="",
        pos=(pos_right, 0),
        height=text_height,
        color=outcome_color,
    )
    outcomes = [outcome_left, outcome_right]

    # Explicit phase TextStims
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

    # save all pre-made visual elements
    visual_elements = dict(
        images=images,
        bg_rects=bg_rects,
        outcomes=outcomes,
        explicit=explicit,
        fb_rects=fb_rects,
    )
    exp_info["visual_elements"] = visual_elements

    ####
    # Instructions
    ###

    ## Training phase
    n_slides = 3
    instr_slides_training = [
        TextSlide(
            win=win,
            text=(
                f"Instructions: Training Phase\n"
                + f"Slide {i + 1}/{n_slides} text.\n\n"
                + f'({exp_info["buttons"]["button_instr_previous"].capitalize()}) Previous - '
                + f'({exp_info["buttons"]["button_instr_next"].capitalize()}) Next - '
                + f'({exp_info["buttons"]["button_instr_skip"].capitalize()}) Skip'
                + (
                    f' - ({exp_info["buttons"]["button_instr_finish"].capitalize()}) Continue with task'
                    if i == (n_slides - 1)
                    else ""
                )
            ),
            height=exp_info["text_height"],
            color=exp_info["text_color"],
        )
        for i in range(n_slides)
    ]

    ## Learning phase
    n_slides = 3
    instr_slides_learning = [
        TextSlide(
            win=win,
            text=(
                f"Instructions: Learning Phase\n"
                + f"Slide {i + 1}/{n_slides} text.\n\n"
                + f'({exp_info["buttons"]["button_instr_previous"].capitalize()}) Previous - '
                + f'({exp_info["buttons"]["button_instr_next"].capitalize()}) Next - '
                + f'({exp_info["buttons"]["button_instr_skip"].capitalize()}) Skip'
                + (
                    f' - ({exp_info["buttons"]["button_instr_finish"].capitalize()}) Continue with task'
                    if i == (n_slides - 1)
                    else ""
                )
            ),
            height=exp_info["text_height"],
            color=exp_info["text_color"],
        )
        for i in range(n_slides)
    ]

    ## Transfer phase
    n_slides = 3
    instr_slides_transfer = [
        TextSlide(
            win=win,
            text=(
                f"Instructions: Transfer Phase\n"
                + f"Slide {i + 1}/{n_slides} text. No more feedback!\n\n"
                + f'({exp_info["buttons"]["button_instr_previous"].capitalize()}) Previous - '
                + f'({exp_info["buttons"]["button_instr_next"].capitalize()}) Next - '
                + f'({exp_info["buttons"]["button_instr_skip"].capitalize()}) Skip'
                + (
                    f' - ({exp_info["buttons"]["button_instr_finish"].capitalize()}) Continue with task'
                    if i == (n_slides - 1)
                    else ""
                )
            ),
            height=exp_info["text_height"],
            color=exp_info["text_color"],
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
                + f'({exp_info["buttons"]["button_instr_previous"].capitalize()}) Previous - '
                + f'({exp_info["buttons"]["button_instr_next"].capitalize()}) Next - '
                + f'({exp_info["buttons"]["button_instr_skip"].capitalize()}) Skip'
                + (
                    f' - ({exp_info["buttons"]["button_instr_finish"].capitalize()}) Continue with task'
                    if i == (n_slides - 1)
                    else ""
                )
            ),
            height=exp_info["text_height"],
            color=exp_info["text_color"],
        )
        for i in range(n_slides)
    ]

    ######################
    ## Start experiment ##
    ######################

    def run_phase(phase, conditions, instruction_slides, exp_info, exp, win):
        """Runs a single phase of the task.

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

                trials_block = conditions_phase.loc[conditions_phase["block"] == block]
                if exp_info["temporal_arrangement"] == "interleaved":
                    trials_block = trials_block.sample(frac=1)
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

    n_repeats = 0
    repeat_training = True
    while repeat_training and n_repeats <= training_n_repeats_max:
        run_phase(
            phase="training",
            conditions=conditions,
            instruction_slides=instr_slides_training,
            exp_info=exp_info,
            exp=exp,
            win=win,
        )

        # Show training repetition dialogue
        response = SlideShow(
            win=win,
            slides=[
                TextSlide(
                    win=win,
                    text=f"Mit '{exp_info['buttons']['button_instr_repeat'].capitalize()}' Training wiederholen\n\n"
                    + f"oder\n\nmit '{exp_info['buttons']['button_instr_finish'].capitalize()}' fortfahren.",
                    height=exp_info["text_height"],
                    color=exp_info["text_color"],
                ),
            ],
            keys_finish=[
                exp_info["buttons"]["button_instr_finish"],
                exp_info["buttons"]["button_instr_repeat"],
            ],
        ).run()

        if not exp_info["buttons"]["button_instr_repeat"] in response:
            repeat_training = False
        else:
            n_repeats += 1
            if n_repeats > training_n_repeats_max:
                response = SlideShow(
                    win=win,
                    slides=[
                        TextSlide(
                            win=win,
                            text=f"Sie haben bereits die maximale Anzahl an Wiederholungen der Übungsrunde erreicht.\n\nMit "
                            + f"'{exp_info['buttons']['button_instr_finish'].capitalize()}' beginnen.",
                            height=exp_info["text_height"],
                            color=exp_info["text_color"],
                        ),
                    ],
                    keys_finish=[exp_info["buttons"]["button_instr_finish"]],
                ).run()

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
    end_screen = visual.TextStim(
        win,
        end_screen_message
        + f"\n\n'{exp_info['buttons']['button_quit'].capitalize()}' to quit.",
        height=exp_info["text_height"],
        color=exp_info["text_color"],
    )
    end_screen.draw()
    win.flip()

    ## Wait for keypress
    event.waitKeys(keyList=[exp_info["buttons"]["button_quit"]])

    # Finish the experiment
    core.quit()
