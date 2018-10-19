# Signal visualization tool in dash

This is a signal visualization tool created with [dash](https://github.com/plotly/dash) in python 3 with the [CSS Boostrap template](https://codepen.io/chriddyp/pen/bWLwgP.css) to provide the style to the html layout.

This tool is aimed to provide quick data visualization tools for signals gathered from sensors (they can be sensors mounted in aircraft, ground vehicles, electric installations, buildings, etc). It also provides the most important features such us moving average filtering of signals, time filtering, and statistics of the signals.

To run the program and start the server:

* Run in the terminal ```python signal_visualization_tool_dash.py``` and the program will start to get and post requests to interact into a local address.
* Copy the url of the local address into your browser. For example: http://000.0.0.1:0000/.

Once run, to interact with the program:

1. Write the path of your local computer where the data files you want to visualize are located.
2. Select the ```.csv``` file you want to analyze. Only ```.csv``` files can be opened with this program.
3. Start selecting signals to plot as a function of time in the left-side figure.
4. Start selecting signals to represent one as a function of the other one in the right-side figure.
5. Use normalization, moving-average filtering, and time filtering to study your signals.
6. After that, you can export your figures with the build-in function of [dash](https://github.com/plotly/dash).

Thank you to [Chris Parmer](https://github.com/chriddyp) and his awesome team for such an incredible library to create data visualization interactive dashboards!
