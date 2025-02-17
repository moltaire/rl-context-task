#!/usr/bin/env python3
import argparse
import numpy as np
from moviepy.editor import VideoClip
from PIL import Image

def displacement_piecewise(t, T, total_offset, aT, dT):
    """
    Compute the displacement (in pixels) at time t using a piecewise function
    with acceleration, constant speed, and deceleration phases.
    """
    T_const = T - aT - dT  # constant speed phase duration
    # Compute maximum speed so that the total displacement is achieved:
    v_max = total_offset / (T_const + 0.5 * (aT + dT))
    if t < aT:
        # Acceleration phase: quadratic ease-in
        return 0.5 * (v_max / aT) * (t ** 2)
    elif t < aT + T_const:
        # Constant speed phase: linear motion
        return 0.5 * v_max * aT + v_max * (t - aT)
    else:
        # Deceleration phase: quadratic ease-out
        t_prime = t - (aT + T_const)
        return (0.5 * v_max * aT +
                v_max * T_const +
                v_max * t_prime -
                0.5 * (v_max / dT) * (t_prime ** 2))

def main():
    parser = argparse.ArgumentParser(
        description="Create a slot machine style animation from an image."
    )
    parser.add_argument("--input", type=str, default="1.png", help="Input image file")
    parser.add_argument("--output", type=str, default="output.mp4", help="Output mp4 file")
    parser.add_argument("--duration", type=float, default=2, help="Animation duration in seconds")
    parser.add_argument("--rotation_speed", type=float, default=1600.0,
                        help="Average rotation speed in pixels per second")
    parser.add_argument("--axis", type=str, choices=["vertical", "horizontal"], default="vertical",
                        help="Axis along which to roll the image")
    parser.add_argument("--fps", type=int, default=60, help="Frames per second for the output video")
    parser.add_argument("--acceleration_duration", type=float, default=0.1,
                        help="Acceleration phase duration in seconds (optional)")
    parser.add_argument("--deceleration_duration", type=float, default=0.1,
                        help="Deceleration phase duration in seconds (optional)")
    args = parser.parse_args()

    # --- Load and prepare the image ---
    # Force conversion to RGB to avoid issues with alpha or palette modes.
    pil_img = Image.open(args.input).convert("RGB")
    img = np.array(pil_img)
    height, width = img.shape[:2]

    # --- Compute overall displacement ---
    total_offset = args.rotation_speed * args.duration

    # --- Define the displacement function ---
    # Use piecewise acceleration/deceleration if both durations are provided
    if (args.acceleration_duration is not None and args.deceleration_duration is not None and
            (args.acceleration_duration + args.deceleration_duration) < args.duration):
        def displacement_func(t):
            return displacement_piecewise(t, args.duration, total_offset,
                                          args.acceleration_duration, args.deceleration_duration)
    else:
        # Otherwise, use a cosine ease-in/out function
        def displacement_func(t):
            progress = 0.5 - 0.5 * np.cos(np.pi * t / args.duration)
            return total_offset * progress

    # --- Function to generate each video frame ---
    def make_frame(t):
        # Compute current offset (in pixels)
        offset = int(displacement_func(t))
        # Roll the image; np.roll automatically wraps around the array.
        if args.axis == "vertical":
            frame = np.roll(img, offset, axis=0)
        else:
            frame = np.roll(img, offset, axis=1)
        # Ensure the frame is uint8 (3-channel RGB)
        return frame.astype(np.uint8)

    # --- Create and write the video clip ---
    clip = VideoClip(make_frame, duration=args.duration)
    clip.write_videofile(args.output, fps=args.fps, codec="libx264")

if __name__ == "__main__":
    main()
