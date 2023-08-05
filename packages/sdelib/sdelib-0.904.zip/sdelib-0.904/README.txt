sdelib is a Python package (written in Python 3.5) for performing various actions on Ito stochastic differential equations (SDE). These actions include:
1) Input SDEs as SDEprob objects.
2) Solve SDEs with an SDEint class that performs numerical Ito integration on SDEprob objects.
3) Estimate strong and weak orders of convergence through a SDEanalysis class
4) Perform these actions either through creating a Python script which uses the above classes, or running gui.py which allows you to perform these actions quickly through a GUI.

sdelib was written as part of a Master's thesis and is intended to be able to do simple actions on SDEs without requiring a lot of coding to do so.

Install instructions:
1) Have Python 3.5 or later installed. May function for Python 3.1-3.4, but won't work for Python 2.
2) Download all files to some folder, for instance C:\sdelib\.
3) For package to work through "import sdelib", "sys.path('C:\\sdelib')"