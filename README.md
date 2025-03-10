Install virtual environemnt with requirements.txt and python 3.9

Soil humidity index takes 4 parameters - rain, humidity, temperature and wind speed. If the index is higher than 2, soil shouldn't be irrigated. Of course, this is very generalized index, so it shouldn't be taken for granted.
Code generates result as a table on web and on Sense Hat Simulator as green colored text if soil should be irrigated and red if it shouldn't. Since the result is first generated on Sense Hat Simulator, it takes up to 10 seconds to show the table.

