.. image:: https://travis-ci.org/timcera/tstoolbox.svg?branch=master
    :target: https://travis-ci.org/timcera/tstoolbox
    :height: 20

.. image:: https://coveralls.io/repos/timcera/tstoolbox/badge.png?branch=master
    :target: https://coveralls.io/r/timcera/tstoolbox?branch=master
    :height: 20

.. image:: https://img.shields.io/pypi/v/tstoolbox.svg
    :alt: Latest release
    :target: https://pypi.python.org/pypi/tstoolbox

.. image:: http://img.shields.io/badge/license-BSD-lightgrey.svg
    :alt: tstoolbox license
    :target: https://pypi.python.org/pypi/tstoolbox/

TSToolbox - Quick Guide
=======================
The tstoolbox is a Python script to manipulate time-series on the command line
or by function calls within Python.  Uses pandas (http://pandas.pydata.org/)
or numpy (http://numpy.scipy.org) for any heavy lifting.

Requirements
------------
* pandas - on Windows this is part scientific Python distributions like
  Python(x,y), Anaconda, or Enthought.

* mando - command line parser

Installation
------------
Should be as easy as running ``pip install tstoolbox`` or ``easy_install
tstoolbox`` at any command line.  Not sure on Windows whether this will bring
in pandas, but as mentioned above, if you start with scientific Python
distribution then you shouldn't have a problem.

Usage - Command Line
--------------------
Just run 'tstoolbox --help' to get a list of subcommands

  accumulate
            Calculates accumulating statistics.
  
  add_trend
            Adds a trend.
  
  aggregate
            Takes a time series and aggregates to specified
            frequency, outputs to 'ISO-8601date,value' format.
  
  calculate_fdc
            Returns the frequency distribution curve. DOES NOT
            return a time-series.
  
  clip
            Returns a time-series with values limited to [a_min,
            a_max]
  
  convert
            Converts values of a time series by applying a factor
            and offset. See the 'equation' subcommand for a
            generalized form of this command.
  
  date_slice
            Prints out data to the screen between start_date and
            end_date
  
  describe
            Prints out statistics for the time-series.
  
  dtw
            Dynamic Time Warping (beta)
  
  equation
            Applies <equation> to the time series data. The
            <equation> argument is a string contained in single
            quotes with 'x' used as the variable representing the
            input. For example, '(1 - x)*sin(x)'.
  
  fill
            Fills missing values (NaN) with different methods.
            Missing values can occur because of NaN, or because
            the time series is sparse. The 'interval' option can
            insert NaNs to create a dense time series.
  
  filter
            Apply different filters to the time-series.
  
  normalization
            Returns the normalization of the time series.
    
  pca
            Returns the principal components analysis of the time
            series. Does not return a time-series. (beta)
  
  peak_detection
            Peak and valley detection.
  
  pick
            Will pick a column or list of columns from input.
            Start with 1.
  
  plot
            Plots.
  
  read
            Collect time series from a list of pickle or csv files
            then print in the tstoolbox standard format.
  
  remove_trend
            Removes a 'trend'.
 
  replace
            Return a time-series replacing values with others.

  rolling_window
            Calculates a rolling window statistic.
  
  stack
            Returns the stack of the input table.
  
  stdtozrxp
            Prints out data to the screen in a WISKI ZRXP format.
  
  tstopickle
            Pickles the data into a Python pickled file. Can be
            brought back into Python with 'pickle.load' or
            'numpy.load'. See also 'tstoolbox read'.
  
  unstack
            Returns the unstack of the input table.
  
The default for all of the subcommands is to accept data from stdin (typically
a pipe).  If a subcommand accepts an input file for an argument, you can use
"--input_ts=input_file_name.csv", or to explicitly specify from stdin (the
default) "--input_ts='-'" .  

For the subcommands that output data it is printed to the screen and you can
then redirect to a file.

Usage - API
-----------
You can use all of the command line subcommands as functions.  The function
signature is identical to the command line subcommands.  The return is always
a PANDAS DataFrame.  Input can be a CSV or TAB separated file, or a PANDAS
DataFrame and is supplied to the function via the 'input_ts' keyword.

Simply import tstoolbox::

    from tstoolbox import tstoolbox

    # Then you could call the functions
    ntsd = tstoolbox.fill(method='linear', input_ts='tests/test_fill_01.csv')

    # Once you have a PANDAS DataFrame you can use that as input to other 
    # tstoolbox functions.
    ntsd = tstoolbox.aggregate(statistic='mean', agg_interval='daily', input_ts=ntsd)

