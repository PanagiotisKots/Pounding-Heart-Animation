import time
import math
from colorama import init

# Initialize colorama to handle ANSI escape codes on Windows
init()

# Define ANSI color codes for different deep red shades (blood-like colors)
colors = [
    "\x1b[38;2;139;0;0m",     # Dark Red (Blood Red)
    "\x1b[38;2;178;34;34m",   # Firebrick
    "\x1b[38;2;220;20;60m",   # Crimson
    "\x1b[38;2;255;0;0m",     # Bright Red (for highlights)
    "\x1b[0m"                 # Reset
]

def main():
    # Clear screen and hide cursor
    print("\x1b[2J\x1b[?25l", end='')
    zb = [0.0] * 100 * 40

    t = 0.0
    rotation_angle = 0.0  # Initialize rotation angle
    while True:
        # Clear screen at the start of each frame
        print("\x1b[H", end='')  # Move to the top instead of clearing the screen

        maxz, c, s = 0, math.cos(rotation_angle), math.sin(rotation_angle)
        y = -0.5

        # Use a sine wave for a more realistic beating effect
        beat_scale = 0.4 + 0.1 * math.sin(t * 5)  # Beating effect
        while y <= 0.5:
            r = beat_scale + 0.05 * math.pow(0.5 + 0.5 * math.sin(t * 6 + y * 2), 8)
            x = -0.5
            while x <= 0.5:
                # Heart formula
                z = -x * x - math.pow(1.2 * y - abs(x) * 2 / 3, 2) + r * r
                if z >= 0:
                    z = math.sqrt(z) / (2 - y)
                    tz = -z
                    while tz <= z:
                        # Rotate
                        nx = x * c - tz * s
                        nz = x * s + tz * c

                        # Add perspective
                        p = 1 + nz / 2
                        vx = round((nx * p + 0.5) * 80 + 10)
                        vy = round((-y * p + 0.5) * 39 + 2)
                        idx = vx + vy * 100
                        if 0 <= idx < len(zb) and zb[idx] <= nz:
                            zb[idx] = nz
                            if maxz < nz:
                                maxz = nz
                        tz += z / 6
                x += 0.01
            y += 0.01

        # Render the heart with colored depth levels
        for i in range(100 * 40):
            if i % 100 == 0:
                print("\n", end='')
            else:
                intensity = round(zb[i] / maxz * 13)  # Determine intensity
                if intensity == 0:
                    print(" ", end='')  # Empty space
                else:
                    # Apply color based on intensity and print character
                    color = colors[min(3, intensity // 3)]  # Select color from the list
                    char = " .,-~:;=!*#$@@"[intensity]      # Select character based on intensity
                    print(f"{color}{char}\x1b[0m", end='')  # Print colored character
            zb[i] = 0  # Reset for next frame

        # Print text below the heart
        print("\n" + " " * 5 + "--------------------------------------")
        print(" " * 5 + "made by: Panagiotis Kotsorgios")
        print(" " * 5 + "made for: Ntina")
        print(" " * 5 + "language: Python3")
        print(" " * 5 + "Description: A console based pounding \n" " " * 5 + "heart animation")
        print("\n" + " " * 5 + "--------------------------------------")

        t += 0.01  # Increase the time increment for smoother transitions
        rotation_angle += 0.05  # Continuously increase rotation angle
        time.sleep(0.01)  # Maintain a steady frame rate

if __name__ == "__main__":
    main()
