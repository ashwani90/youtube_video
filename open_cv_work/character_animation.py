import numpy as np

def ease_in_out(t):
    return t * t * (3 - 2 * t)  # Smoothstep easing function

def animate_character(start, end, duration, fps=30):
    frames = int(duration * fps)
    positions = []

    for i in range(frames):
        t = ease_in_out(i / frames)
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        positions.append((int(x), int(y)))
    
    return positions


