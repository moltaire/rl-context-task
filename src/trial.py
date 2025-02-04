import numpy as np
from os.path import join
from psychopy import event, core


class Trial(object):
    """Runs a single trial of the RL Context task."""

    def __init__(self, trial_info, exp, exp_info, win, visual_elements):
        super(Trial, self).__init__()
        self.trial_id = trial_info["trial_id"]
        self.block = trial_info["block"]
        self.feedback = trial_info["feedback"]  # partial, complete, none
        self.image1 = trial_info["image1"]
        self.image2 = trial_info["image2"]
        self.outcome1 = trial_info["outcome1"]
        self.outcome2 = trial_info["outcome2"]
        self.stim1pos = trial_info["stim1pos"]
        self.exp = exp
        self.win = win
        self.exp_info = exp_info
        self.rects = visual_elements["rects"]
        self.outcomeStims = visual_elements["outcomes"]
        self.imageStims = visual_elements["images"]

    def prepare(self):
        # Set up images and outcomes
        # TODO: make left-right shuffle
        for imageStim, image in zip(self.imageStims, (self.image1, self.image2)):
            imageStim.setImage(join("stim", "images", image))

        # Set up outcomes
        # TODO: make left-right shuffle
        for outcomeStim, outcome in zip(
            self.outcomeStims, (self.outcome1, self.outcome2)
        ):
            outcomeStim.setText(outcome)

    def run(self):

        # Stimulus phase
        for image in self.imageStims:
            image.draw()

        ## Show stimuli and wait for response
        rt_start = self.win.flip()

        # Choice phase
        ## When a choice was made, show the feedback frame for 500 ms

        response = event.waitKeys(
            keyList=[
                self.exp_info["buttons"]["button_left"],
                self.exp_info["buttons"]["button_right"],
                self.exp_info["buttons"]["button_quit"],
            ],
            maxWait=self.exp_info["choice_timeout"],
            timeStamped=rt_start,
        )

        ## decode first response
        if response is not None:
            print(response)
            # participant pressed a button
            if response[0][0] in [self.exp_info["buttons"]["button_quit"]]:
                print("User quit experiment.")
                core.quit()
            timed_out = False
            key, rt = response[0]
            if self.stim1pos == "left":
                if key == self.exp_info["buttons"]["button_left"]:
                    choice = 1
                elif key == self.exp_info["buttons"]["button_right"]:
                    choice = 2
            elif self.stim1pos == "right":
                if key == self.exp_info["buttons"]["button_left"]:
                    choice = 2
                elif key == self.exp_info["buttons"]["button_right"]:
                    choice = 1
            else:
                raise ValueError(
                    f"`stim1pos` must be 'left' or 'right' (is '{self.stim1pos}')."
                )
        else:
            # no button was pressed
            timed_out = True
            key, rt = (None, None)
            choice = np.nan
        self.choice = choice
        self.rt = rt
        print(choice, rt)

        ## Show choice frame
        for image in self.imageStims:
            image.draw()
        self.rects[choice - 1].draw()
        self.win.flip()
        core.wait(0.5)

        ## Show outcome(s)
        if not self.feedback == "none":
            if self.feedback == "complete":
                [outcomeStim.draw() for outcomeStim in self.outcomeStims]
            elif self.feedback == "partial":
                if not timed_out:
                    self.outcomeStims[choice - 1].draw()  # draw chosen option outcome
                    self.imageStims[1 - (choice - 1)].draw()  # draw other image
                else:
                    [
                        imageStim.draw() for imageStim in self.imageStims
                    ]  # draw both images if timed out
            else:
                raise ValueError(
                    f"`feedback` must be one of ['complete', 'partial', 'none'], but is '{self.feedback}'."
                )
            self.win.flip()
            core.wait(1)

    def log(self):
        ## Log information
        self.exp.addData("trial", self.trial_id)
        self.exp.addData("block", self.block)
        self.exp.addData("choice", self.choice)
        self.exp.addData("rt", self.rt)
        self.exp.nextEntry()
