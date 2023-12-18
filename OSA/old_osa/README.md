Graphical User Interface program to control the Ando AQ-6315A Optical Spectrum Analyzer.
The one we have in our lab is working perfectly, but the buttons on the front does not work as it is from 1996. This program is meant to be used instead of the front panel for the most occuring and simplest cases.

It is implemented using a model-view-controller design pattern to ensure that what we see is what is the case in the OSA. 
Run the run.py file to start the program 

The program requires communication with the OSA through the GPIB interface using a [blue NI cable](https://se.farnell.com/productimages/large/en_GB/3621012-40.jpg) , however someone motivated can add other communication protocals and/or support for the more affordable [prologix cables](https://i0.wp.com/prologix.biz/wp-content/uploads/2023/07/Ethernet-front_zoom.jpg?fit=730%2C730&ssl=1). 

The files are saved as .csv with ','-delimiter. If filename "test" is saved, the filename will be "test_x.csv" where x is either A, B or C. The user has to select which traces to save in the bottom panel. 

As retrieving traces from the OSA is a quite time-consuming activity, this is moved to another thread, however the program can still seem to "freeze" as a little bit as it is talking to the OSA. Perhaps other protocols than GPBI are faster.

Dependencies: Tkinter, numpy, pyvisa, matplotlib, Queue, threading, csv. Most of these are standard python-modules however pyvisa for example must be installed with pip. 

![example view of the program](/OSA/old_osa/example.png)
