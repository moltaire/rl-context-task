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
        self.symbol1 = trial_info["symbol1"]
        self.symbol2 = trial_info["symbol2"]
        self.outcome1 = trial_info["outcome1"]
        self.outcome2 = trial_info["outcome2"]
        self.symbol1pos = trial_info["symbol1pos"]
        self.exp = exp
        self.win = win
        self.exp_info = exp_info
        self.rects = visual_elements["rects"]
        self.outcomeStims = visual_elements["outcomes"]
        self.imageStims = visual_elements["images"]

    def prepare(self):
        """
        Updates the visual elements to use information from current `trial_info`.
        """
        # Set up images and outcomes
        for imageStim, symbol in zip(self.imageStims, (self.symbol1, self.symbol2)):
            imageStim.setImage(
                join("stim", "images", self.exp_info["stimulus_map"][symbol])
            )

        # Set up outcomes
        for outcomeStim, outcome in zip(
            self.outcomeStims, (self.outcome1, self.outcome2)
        ):
            outcomeStim.setText(outcome)

        # Set positions
        if self.symbol1pos == "left":
            self.imageStims[0].setPos((self.exp_info["pos_left"], 0))
            self.imageStims[1].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[0].setPos((self.exp_info["pos_left"], 0))
            self.outcomeStims[1].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[0]
        elif self.symbol1pos == "right":
            self.imageStims[0].setPos((self.exp_info["pos_right"], 0))
            self.imageStims[1].setPos((self.exp_info["pos_left"], 0))
            self.outcomeStims[0].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[1].setPos((self.exp_info["pos_left"], 0))
        else:
            raise ValueError(
                f"`symbol1pos` must be 'left' or 'right' (is '{self.symbol1pos}')."
            )

    def run(self):

        # Stimulus phase
        for image in self.imageStims:
            image.draw()

        ## Show stimuli and wait for response
        rt_start = self.win.flip()

        # Serial port trigger example
        # if self.exp_info["serial_port"] is not None:
        #     self.exp_info["serial_port"].send_trigger(f"trial_{self.trial_id}_stimuli-on")

        # Choice phase
        ## When a choice was made, show the feedback frame for 500 ms

        keyEvents = event.waitKeys(
            keyList=[
                self.exp_info["buttons"]["button_left"],
                self.exp_info["buttons"]["button_right"],
                self.exp_info["buttons"]["button_quit"],
            ],
            maxWait=self.exp_info["duration_timeout"],
            timeStamped=rt_start,
        )

        ## decode first response
        if keyEvents is not None:
            print(keyEvents)
            # participant pressed a button
            if keyEvents[0][0] in [self.exp_info["buttons"]["button_quit"]]:
                print("User quit experiment.")
                core.quit()
            timed_out = False
            key_pressed, rt = keyEvents[0]

            # decode into response (left or right)
            if key_pressed == self.exp_info["buttons"]["button_left"]:
                response = "left"
            elif key_pressed == self.exp_info["buttons"]["button_right"]:
                response = "right"
            else:
                print(key)

            # decode into choice (1 or 2)
            if self.symbol1pos == "left":
                if response == "left":
                    choice = 1
                elif response == "right":
                    choice = 2
                else:
                    raise ValueError(response)
            elif self.symbol1pos == "right":
                if response == "left":
                    choice = 2
                elif response == "right":
                    choice = 1
                else:
                    raise ValueError(response)
            else:
                raise ValueError(
                    f"`symbol1pos` must be 'left' or 'right' (is '{self.symbol1pos}')."
                )
        else:
            # no button was pressed
            timed_out = True
            key_pressed, rt = (np.nan, np.nan)
            response = np.nan
            choice = np.nan
        self.choice = choice
        self.rt = rt
        self.response = response

        ## Show choice frame (if not timed out)
        if not timed_out:

            ### Draw both images
            for image in self.imageStims:
                image.draw()

            ### Draw rectangle of chosen option
            self.rects[
                response == "right"
            ].draw()  # will draw left rect if response == "left" and right rect if response == "right"
            self.win.flip()
            core.wait(self.exp_info["duration_choice"])  # TODO: move to exp_info

            ## Show outcome(s)
            if not self.feedback == "none":
                if self.feedback == "complete":
                    [outcomeStim.draw() for outcomeStim in self.outcomeStims]
                elif self.feedback == "partial":
                    self.outcomeStims[choice - 1].draw()  # draw chosen option outcome
                    self.imageStims[1 - (choice - 1)].draw()  # draw other option image
                else:
                    raise ValueError(
                        f"`feedback` must be one of ['complete', 'partial', 'none'], but is '{self.feedback}'."
                    )
                self.win.flip()
                core.wait(self.exp_info["duration_outcome"])  # TODO: move to exp_info
        else:  # timed out
            pass  # do nothing?

        # Show ITI
        self.win.flip()
        core.wait(self.exp_info["duration_iti"])

    def log(self):
        ## Log information
        self.exp.addData("trial", self.trial_id)
        self.exp.addData("block", self.block)
        self.exp.addData("choice", self.choice)
        self.exp.addData("rt", self.rt)
        self.exp.nextEntry()
