# y2proj
Every file has a module docstring, but here is an outline:

USAGE:
    Main results were generated using physics.py. The functions in here will take quite a long time to run with the parameters at their current settings. 
    
    For the figures in the report:

    Figure1: plotPV(num_balls=60, ballsize=0.01), set the run time using parameters on lines 26 and 27. check_collide(n) will run the system until time is *n* in seconds. pressure(n) will gather data for *n* seconds. For the report 5 and 20 were used.

    Figure2: plotPV(num_balls=27, ballsize=1.9). Lines 26 and 27 parameters were 2 and 5.

    Figure3: plotMaxwellB(). Parameters set on lines 87-89. The ones seen here were the ones used for the report. To run the system for less time, reduce the factor of 5 at the start of line 102.

    Figure4: brownGen(). The frame rate, as set in core.py, defaults to 50fps, so adjust the number of frames on line 144 accordingly. Both the animation and the particle track are saved in the current working directory. Since this takes a long time to run, I have made an animation generated using this function available at https://github.com/millsyman/y2proj/blob/master/brownian.mp4
    The entire project code with commit history is also available here should you need it for any reason. Alternatively, brownTest() in testing.py only runs 4 seconds of simulation time, so should run much faster.

    Again, these all take quite a while, so if you want to verify that they are working it may well be worth reducing some of the parameters to save time.

OTHER FUNCTIONS:
    testing.py was written as a testing suite for the project. This was intended to either be run with command line parameters or imported and used interactively.

    Example Terminal/CMD Usage:
        python ./testing.py s d 20
    This would (assuming you are in the correct working directory) run an animation with 4 balls and a logging level of 20. Unless you are trying to look at the internals, 20 is a pretty good logging level to go with. Logs are written to timestamped files in the current working directory.

    For full usage please refer to the module and function docstrings.

CODE STRUCTURE:
    objects.py:
        Contains classes Ball and Container. Represent objects in the system

    system.py:
        Container class System. Contains all objects, manages time and animation.

    core.py:
        Helper functions and constants. Also logging.

    testing.py:
        Testing suite

    physics.py:
        Described above

    diatomic.py:
        Reuses code from physics.py to simulate a diatomic gas.
