
This is a plugin for the Spyder IDE that integrates the Python memory profiler.
It allows you to see the memory usage in every line.

Usage
-----

Add a ``@profile`` decorator to the functions that you wish to profile then
press Ctrl+Shift+F10 to run the profiler on the current script, or go to
``Run > Profile memory line by line``.

The results will be shown in a dockwidget, grouped by function. Lines with a
stronger color have the largest increments in memory usage.


