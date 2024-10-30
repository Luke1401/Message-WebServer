# Comparison time between single threaded and multi threaded server

This is the comparison plot I got after run the file boxplot.py
#
![Time Comparison](./comparisonPlot.png?raw=true)

As seen in above, you can see that the single-threaded and multi-threaded results are mostly the same, the time result mostly around 0.07(seconds) and the multi-threaded server sometimes got around 0.2(seconds) at some moment while the server is running.
- Multi-threaded server got the highest time result which is approximately 6.2(seconds) while single-threaded server got the highest time result which is approximately 1.2(seconds).

As most of the results took about less than a second for 100 requests, but we still notice some outliers which may caused by the speed of internet from my home.