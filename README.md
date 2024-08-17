# AprilTag_Localization_Coprocess

## Overview

The **AprilTag_Localization_Coprocess** is a Python-based software designed for AprilTag detection, serving as the coprocessor for Team 114's FRC robot during the 2023-2024 season. The software acts as an intermediary between the AprilTag/OpenCV libraries running on a coprocessor, and the robot computer.

## Features

- **Multiple Camera Support**: Can simultaneously process input from multiple cameras for more accurate localization.
- **Multiprocess AprilTag Detection**: Utilizes Python's multiprocessing capabilities to handle detection tasks in parallel, improving performance. Capable of handling two monochrome cameras simultaneously at 1280x720p @ 50fps on RP5.
- **Socket Communication**: Employs socket-based communication for interaction with the main robot system.

## Known Bugs

- **Intermittent Issue**: Occasionally returns stale pose data. The issue has been traced to the `detect_pose()` function call in the AprilTag library.
