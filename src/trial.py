import numpy as np
from os.path import join
from psychopy import event, core


class Trial(object):
    """Runs a single trial of the RL Context task."""

    def __init__(self, trial_info, exp, exp_info, win, visual_elements):
        super(Trial, self).__init__()
        self.trial_info = trial_info
        self.exp = exp
        self.win = win
        self.exp_info = exp_info
        self.bg_rects = visual_elements["bg_rects"]
        self.fb_rects = visual_elements["fb_rects"]
        self.outcomeStims = visual_elements["outcomes"]
        self.imageStims = visual_elements["images"]
        self.explicitStims = visual_elements["explicit"]

    def prepare(self):
        """
        Updates the visual elements to use information from current `trial_info`.
        """
        if self.trial_info["phase"] != "explicit":
            # Set up images and outcomes
            for i, (imageStim, symbol) in enumerate(
                zip(
                    self.imageStims,
                    (self.trial_info["symbol1"], self.trial_info["symbol2"]),
                )
            ):
                imagePath = join(
                    "stim", "images", self.exp_info["stimulus_map"][symbol]
                )
                # save images that were shown
                imageStim.setImage(imagePath)
                self.trial_info[f"image{i+1}"] = imagePath

            # Set up outcomes
            for outcomeStim, outcome in zip(
                self.outcomeStims,
                (self.trial_info["outcome1"], self.trial_info["outcome2"]),
            ):
                outcomeStim.setText(outcome)

        else:  # Explicit phase: Set up text stimuli
            for explicitStim, probability, outcome in zip(
                self.explicitStims,
                [self.trial_info["probability1"], self.trial_info["probability2"]],
                [self.trial_info["outcome1"], self.trial_info["outcome2"]],
            ):
                explicitStim.setText(
                    f"{(probability * 100):.0f}%\n\n{outcome:.0f} Pkt."
                )
                # log that no images were shown
                self.trial_info["image1"] = np.nan
                self.trial_info["image2"] = np.nan

        # Set positions
        if self.trial_info["symbol1pos"] == "left":
            self.imageStims[0].setPos((self.exp_info["pos_left"], 0))
            self.imageStims[1].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[0].setPos((self.exp_info["pos_left"], 0))
            self.outcomeStims[1].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[0]
        elif self.trial_info["symbol1pos"] == "right":
            self.imageStims[0].setPos((self.exp_info["pos_right"], 0))
            self.imageStims[1].setPos((self.exp_info["pos_left"], 0))
            self.outcomeStims[0].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[1].setPos((self.exp_info["pos_left"], 0))
        else:
            raise ValueError(
                f"`symbol1pos` must be 'left' or 'right' (is '{self.trial_info['symbol1pos']}')."
            )

    def run(self):

        # Stimulus phase
        for rect in self.bg_rects:
            rect.draw()
        if self.trial_info["phase"] != "explicit":
            for image in self.imageStims:
                image.draw()
        else:  # explicit phase
            for explicit in self.explicitStims:
                explicit.draw()

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
                raise ValueError(f"An unexpected key was pressed: {key}")

            # decode into choice (1 or 2)
            if self.trial_info["symbol1pos"] == "left":
                if response == "left":
                    choice = 1
                elif response == "right":
                    choice = 2
                else:
                    raise ValueError(response)
            elif self.trial_info["symbol1pos"] == "right":
                if response == "left":
                    choice = 2
                elif response == "right":
                    choice = 1
                else:
                    raise ValueError(response)
            else:
                raise ValueError(
                    f"`symbol1pos` must be 'left' or 'right' (is '{self.trial_info['symbol1pos']}')."
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

            # Draw background rectangles
            for rect in self.bg_rects:
                rect.draw()
            ### Draw both images
            if self.trial_info["phase"] != "explicit":
                for image in self.imageStims:
                    image.draw()
            else:
                for explicit in self.explicitStims:
                    explicit.draw()

            ### Draw rectangle of chosen option
            self.fb_rects[
                response == "right"
            ].draw()  # will draw left rect if response == "left" and right rect if response == "right"
            self.win.flip()
            core.wait(self.exp_info["duration_choice"])

            ## Show outcome(s) if feedback != "none"
            if not self.trial_info["feedback"] == "none":
                # draw background rectangles
                [bg_rect.draw() for bg_rect in self.bg_rects]

                # draw feedback frame of chosen option
                self.fb_rects[
                    response == "right"
                ].draw()  # will draw left rect if response == "left" and right rect if response == "right"

                # set colors of outcomes
                self.outcomeStims[choice - 1].color = self.exp_info["outcome_color"]
                self.outcomeStims[1 - (choice - 1)].color = self.exp_info[
                    "outcome_color_counterfactual"
                ]

                if self.trial_info["feedback"] == "complete":
                    [outcomeStim.draw() for outcomeStim in self.outcomeStims]
                elif self.trial_info["feedback"] == "partial":
                    self.outcomeStims[choice - 1].draw()  # draw chosen option outcome
                    if self.trial_info["phase"] != "explicit":
                        self.imageStims[
                            1 - (choice - 1)
                        ].draw()  # draw other option image
                    else:  # explicit
                        self.explicitStims[
                            1 - (choice - 1)
                        ].draw()  # draw other option image
                else:
                    raise ValueError(
                        f"`feedback` must be one of ['complete', 'partial', 'none'], but is '{self.trial_info['feedback']}'."
                    )
                self.win.flip()
                core.wait(self.exp_info["duration_outcome"])
            else:  # feedback == "none"
                pass
        else:  # timed out
            pass  # do nothing?

        # compute reward
        if choice == 1:
            reward_t = self.trial_info["outcome1"]
        elif choice == 2:
            reward_t = self.trial_info["outcome2"]
        else:
            reward_t = 0
        self.obtained_reward = reward_t
        if self.trial_info["phase"] != "training":
            self.exp_info["total_reward"] += reward_t
            self.cumulative_reward = self.exp_info["total_reward"]

        # Show ITI
        self.win.flip()
        core.wait(self.exp_info["duration_iti"])

    def log(self):
        ## Copy all information from trial_info
        for var, val in self.trial_info.items():
            self.exp.addData(var, val)

        ## Log information
        self.exp.addData("response", self.response)
        self.exp.addData("choice", self.choice)
        self.exp.addData("rt", self.rt)
        self.exp.addData("obtained_reward", self.obtained_reward)
        self.exp.addData("cumulative_reward", self.exp_info["total_reward"])
        self.exp.nextEntry()
