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
                    "stim",
                    "images",
                    str(self.exp_info["Stimulus-Set"]),
                    self.exp_info["stimulus_map"][symbol],
                )
                # save images that were shown
                imageStim.setImage(imagePath)
                self.trial_info[f"image{i+1}"] = imagePath

        else:  # Explicit phase: Set up text stimuli
            for explicitStim, probability, outcome in zip(
                self.explicitStims,
                [self.trial_info["probability1"], self.trial_info["probability2"]],
                [
                    self.trial_info["potential_outcome1"],
                    self.trial_info["potential_outcome2"],
                ],
            ):
                explicitStim.setText(
                    f"{(float(probability) * 100):.0f}%\n\n{float(outcome):.0f} Pkt."
                )
                # log that no images were shown
                self.trial_info["image1"] = np.nan
                self.trial_info["image2"] = np.nan

        # Prepare outcomes
        ## If `outcome_randomness` is "random", we need to draw `actual_outcome`s according to their probabilities.
        if self.trial_info["outcome_randomness"] == "random":
            # Check that probability info is given
            for p in [self.trial_info["probability1"], self.trial_info["probability2"]]:
                assert isinstance(p, (float, int)) and not np.isnan(
                    p
                ), "If `outcome_randomness` is set to 'random', 'probability' columns in 'conditions.csv' need to be of type float!"

            self.trial_info["actual_outcome1"] = np.random.choice(
                [self.trial_info["potential_outcome1"], 0],
                p=[
                    self.trial_info["probability1"],
                    1 - self.trial_info["probability1"],
                ],
            )
            self.trial_info["actual_outcome2"] = np.random.choice(
                [self.trial_info["potential_outcome2"], 0],
                p=[
                    self.trial_info["probability2"],
                    1 - self.trial_info["probability2"],
                ],
            )
        ## Otherwise, they are read from the actual_outcome columns directly
        elif self.trial_info["outcome_randomness"] == "pseudorandom":
            # just check that actual outcomes are provided
            for o in [
                self.trial_info["actual_outcome1"],
                self.trial_info["actual_outcome2"],
            ]:
                assert isinstance(o, (float, int)) and not np.isnan(
                    o
                ), "If `outcome_randomness` is set to 'pseudorandom', you must provide numerical values in `actual_outcome`s!"
        else:
            raise ValueError(
                f"`outcome_randomness` experiment setting must be one of ['random', 'pseudorandom'], but is '{self.exp_info['outcome_randomness']}'."
            )

        # Prepare outcome feedback
        if self.trial_info["feedback"] == "skip":
            pass
        else:
            if self.trial_info["feedback"] in ["complete", "partial"]:
                ## Content, i.e., reward information
                outcomeContent = (
                    self.trial_info["actual_outcome1"],
                    self.trial_info["actual_outcome2"],
                )
            elif self.trial_info["feedback"] == "none":
                ## show question marks for no feedback (for partial, the unchosen option's content will be updated after choice)
                outcomeContent = ("?", "?")
            else:
                raise ValueError(
                    f"`feedback` must be one of ['complete', 'partial', 'none', 'skip'], but is '{self.trial_info['feedback']}'."
                )

            # Initialize outcome content and color
            for outcomeStim, outcome in zip(
                self.outcomeStims,
                outcomeContent,
            ):
                outcomeStim.setText(outcome)
                # also set color to counterfactual color
                outcomeStim.color = self.exp_info["outcome_color_counterfactual"]

        # Set positions
        if self.trial_info["option1pos"] == "left":
            self.imageStims[0].setPos((self.exp_info["pos_left"], 0))
            self.imageStims[1].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[0].setPos((self.exp_info["pos_left"], 0))
            self.outcomeStims[1].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[0]
        elif self.trial_info["option1pos"] == "right":
            self.imageStims[0].setPos((self.exp_info["pos_right"], 0))
            self.imageStims[1].setPos((self.exp_info["pos_left"], 0))
            self.outcomeStims[0].setPos((self.exp_info["pos_right"], 0))
            self.outcomeStims[1].setPos((self.exp_info["pos_left"], 0))
        else:
            raise ValueError(
                f"`option1pos` must be 'left' or 'right' (is '{self.trial_info['option1pos']}')."
            )

        # Compute trial ITI
        self.iti = np.random.uniform(
            self.exp_info["duration_iti"] - self.exp_info["duration_iti_jitter"] / 2,
            self.exp_info["duration_iti"] + self.exp_info["duration_iti_jitter"] / 2,
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
        ## When a choice was made, show the feedback frame for `duration_choice`
        ## or, if `duration_fixed_response == True` for `duration_timeout` - rt

        keyEvents = event.waitKeys(
            keyList=[
                self.exp_info["buttons"]["button_left"],
                self.exp_info["buttons"]["button_right"],
                self.exp_info["buttons"]["button_quit"],
            ],
            maxWait=self.exp_info["duration_timeout"],
            timeStamped=rt_start,
        )

        ## Decode response
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
                raise ValueError(f"An unexpected key was pressed: {key_pressed}")

            # decode into choice (1 or 2)
            if self.trial_info["option1pos"] == "left":
                if response == "left":
                    choice = 1
                elif response == "right":
                    choice = 2
                else:
                    raise ValueError(response)
            elif self.trial_info["option1pos"] == "right":
                if response == "left":
                    choice = 2
                elif response == "right":
                    choice = 1
                else:
                    raise ValueError(response)
            else:
                raise ValueError(
                    f"`option1pos` must be 'left' or 'right' (is '{self.trial_info['option1pos']}')."
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
        ### TODO: Research casino animation during this phase. Simple way could be pulsing opacity
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
            if not self.exp_info["duration_fixed_response"]:
                core.wait(self.exp_info["duration_choice"])
            else:
                core.wait(self.exp_info["duration_timeout"] - rt)

            ## Show outcome(s) if feedback != "skip"
            if not self.trial_info["feedback"] == "skip":
                # draw background rectangles
                [bg_rect.draw() for bg_rect in self.bg_rects]

                # draw feedback frame of chosen option
                self.fb_rects[
                    response == "right"
                ].draw()  # will draw left rect if response == "left" and right rect if response == "right"

                # For partial or complete feedback, update chosen option outcome's color
                if self.trial_info["feedback"] in ["complete", "partial"]:
                    # chosen outcome color
                    self.outcomeStims[choice - 1].color = self.exp_info["outcome_color"]

                # For partial feedback, occlude unchosen outcome
                if self.trial_info["feedback"] == "partial":
                    self.outcomeStims[1 - (choice - 1)].setText("?")

                # Draw the outcomes
                [outcomeStim.draw() for outcomeStim in self.outcomeStims]

                # Show everything
                self.win.flip()
                core.wait(self.exp_info["duration_outcome"])
            else:  # feedback == "skip"
                pass
        else:  # timed out
            pass  # do nothing?

        # compute reward
        if choice == 1:
            reward_t = self.trial_info["actual_outcome1"]
        elif choice == 2:
            reward_t = self.trial_info["actual_outcome2"]
        else:
            reward_t = 0
        self.obtained_reward = reward_t
        if self.trial_info["phase"] != "training":
            self.exp_info["total_reward"] += reward_t
            self.cumulative_reward = self.exp_info["total_reward"]

        # Show ITI
        ## Trial-specific ITI (in case of `duration_iti_jitter != 0`)
        ## is computed in self.prepare()
        self.win.flip()
        core.wait(self.iti)

    def log(self):
        # Add subject and session information
        self.trial_info["subject"] = self.exp_info["Subject"]
        self.trial_info["session"] = self.exp_info["Session"]

        # Add trial ITI
        self.trial_info["iti"] = self.iti

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
