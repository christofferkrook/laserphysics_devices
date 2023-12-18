Graphical User Interface program to control the Ando AQ-6315A Optical Spectrum Analyzer.
The one we have in our lab is working perfectly, but the buttons on the front does not work as it is from 1996. This program is meant to be used instead of the front panel for the most occuring and simplest cases.

It is implemented using a model-view-controller design pattern to ensure that what we see is what is the case in the OSA. 
Run the run.py file to start the program 

The program requires communication with the OSA through the GPIB interface using a [blue NI cable](https://se.farnell.com/productimages/large/en_GB/3621012-40.jpg) , however someone motivated can add other communication protocals and/or support for the more affordable [prologix cables](https://i0.wp.com/prologix.biz/wp-content/uploads/2023/07/Ethernet-front_zoom.jpg?fit=730%2C730&ssl=1). 
