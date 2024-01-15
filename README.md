## Cheat Sheet Architecture Overview
This program was designed and optimized using Python3 under a WSL terminal in Windows 11, so I would suggest running the program in a WSL terminal. If not, it's not a major issue, though the resolution and formatting might be off while using Windows which is unintended.

There are a total of 7 files needed to run this program properly.

The main script to run is titled "cheatSheetArch.py", and the other files will be used by this main script.

There are two additional Python scripts, "binaryArithAlgos.py" and "conversion.py" that contains the algorithms needed for the Instruction and Arithmetic sections.

There are two txt files, "instructLearnInfo.txt" and "pathLearnInfo.txt", that contain text I wanted to output to the Instruction and Datapath sections. I chose to use separate files for this text, so I can keep my main script file from being bloated.

The last two files are two png files, "welcomeScreen.png" and "datapathDiagram.png", that will display images on the start screenand the Datapath section. 

Outside of that, there is error checking in each section of the program, though I'm not sure if it's 100% bug free. I tested user input for a majority of cases, but there might be a rare case or two I didn't think of.
