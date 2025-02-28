from settings import *
from src import SlideShow, TextSlide, ImageSlide
from os.path import join


def make_instructions(win):
    # ============================ #
    # DON'T CHANGE ANYTHING ABOVE! #
    # ============================ #

    """
    Here, you can define your custom instructions.
    Slides for each experiment phase (training, learning, transfer, explicit, debriefing)
    should be defined in the sections below.
    
    Each should be a list of slide objects (either `TextSlide` or `ImageSlide`).
    
    `TextSlide`s are a little ugly but quick and easy to make.

    `ImageSlide`s just read in existing images from given paths.
    These can make great instructions, e.g., from PowerPoint slides.
    """

    # -------------- #
    # Training phase #
    # -------------- #
    
    ## This template creates 3 TextSlides that contain the slide number
    ## and information on which buttons can be pressed to navigate the instructions.
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

    # -------------- #
    # Learning phase #
    # -------------- #
    ## This template creates ImageSlides from premade image files
    ## in the folder "instructions/learning-phase" called
    ## "rl-context-task_instructions_learning-phase.001.png"
    ## "rl-context-task_instructions_learning-phase.002.png"
    ## "rl-context-task_instructions_learning-phase.003.png"
    
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

    # -------------- #
    # Transfer phase #
    # -------------- #
    ## These are the same as those for the training phase.
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

    # -------------- #
    # Explicit phase #
    # -------------- #
    ## Also conceptually the same as for the training phase.
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

    # ---------- #
    # Debriefing #
    # ---------- #
    ## Debriefing is just one slide here. Note that it must still be a list (using square brackets around it)
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

    # ============================ #
    # DON'T CHANGE ANYTHING BELOW! #
    # ============================ #

    return (
        instr_slides_training,
        instr_slides_learning,
        instr_slides_transfer,
        instr_slides_explicit,
        debriefing_slides,
    )
