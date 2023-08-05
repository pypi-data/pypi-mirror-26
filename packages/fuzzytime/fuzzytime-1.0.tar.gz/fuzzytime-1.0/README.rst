fuzzytime - Fuzzy Timestamp Generator
~~~~~~~~~~~~~~~~~~~~~~
To use, simply type:

from fuzzytime import *

print fuzzytime(x)

Where, 'x' can be a datetime, date, time, epoch (int/float), or Str input containing date input 
separated by '/' or '-' ex. YYYY/MM/DD or YYYY-MM-DD or time input separated by ':' ex. HH:MM:SS.

For something more ridiculous try:

print secondsago(x)

or,

print minutesago(x)
