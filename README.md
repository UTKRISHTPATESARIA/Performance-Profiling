# Performance-Profiling
Profiling a matrix multiplication of different sizes using various tile sizes &amp; loop modifications and comparing against various hardware counters using perf_event_open()

## Using the Tool:

Use python version 3.6+ to run python files, also make sure to install the necessary packages required for running the program.

1) Run the gen_bin.py to create the binaries for the C files.
2) Once binaries are created, run the script.sh to generated the log files.
3) Once the logs are generated, run the generate_plots.py (should be in same folder as that of log files generated above) to generate plots and final data used in the report.
