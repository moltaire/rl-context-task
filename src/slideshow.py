from psychopy import visual, event, core
import numpy as np


class SlideShow(object):
    """
    Present series of TextSlide or ImageSlide
    """

    def __init__(
        self,
        win=None,
        slides=None,
        start_idx=0,
        timeout=float("inf"),
        keys_next=["right"],
        keys_back=["left"],
        keys_quit=["q", "escape"],
        keys_skip=["s"],
        keys_finish=["space"],
    ):
        self.win = win
        if not isinstance(slides, list):
            slides = [slides]
        self.slides = slides
        self.start_idx = start_idx
        self.keys_next = keys_next
        self.keys_back = keys_back
        self.keys_quit = keys_quit
        self.keys_skip = keys_skip
        if keys_finish is None:
            keys_finish = keys_next
        self.keys_finish = keys_finish
        self.key_list = keys_next + keys_back + keys_quit + keys_skip + keys_finish
        self.timeout = timeout

    def run(self):
        position = self.start_idx
        while True:
            self.slides[position].draw()
            self.win.flip()
            key = event.waitKeys(maxWait=self.timeout, keyList=self.key_list)[0]
            if key is not None:
                # Quit everything
                if key in self.keys_quit:
                    print("User quit.")
                    core.quit()
                # If at the last slide, check for finishing keys
                elif (key in self.keys_finish) and (position == len(self.slides) - 1):
                    return key
                # Skip to end
                elif key in self.keys_skip:
                    position = len(self.slides) - 1
                elif key in self.keys_back:
                    position = np.max([0, position - 1])
                elif key in self.keys_next:
                    position += 1
                    if position > len(self.slides) - 1:
                        break
            else:
                position += 1
                if position > len(self.slides) - 1:
                    return self.keys_finish[0]


class TextSlide(object):
    def __init__(self, win=None, text="", **kwargs):
        self.win = win
        self.text = text
        self.kwargs = kwargs
        self._text = visual.TextStim(win=self.win, text=self.text, **self.kwargs)

    def draw(self):
        self._text.draw()


class ImageSlide(object):
    def __init__(self, win=None, image=None, **kwargs):
        self.win = win
        self.image = image
        self.kwargs = kwargs
        self._image = visual.ImageStim(win=win, image=self.image, **self.kwargs)

    def draw(self):
        self._image.draw()
