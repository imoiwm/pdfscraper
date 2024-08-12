# PDFScrape

Originally built for a friend's project.

When scraping a website that doesn't explicitly have an API for grabbing documents or other information,
I made this small script (tailored for their exact context) using Selenium
to parallelize and automate clicking through a bunch of "Click here to download PDF" icons on a child care website ([Example here](https://families.decal.ga.gov/ChildCare/detail/6906)).

Right now provides mostly just a look at how Selenium could be used as an alternative method for grabbing a bunch of PDFs. Instructions below were created solely with my friend's situation in mind.

-----------------------------------------------
Prerequisite downloads:

- Make sure Python is installed
- pdfscraper.py
- Download your provider list from Excel as a .csv file

First, modify the `num_threads` variable to match the number of cores on your CPU.
You can check how many cores there are by running the following lines in Python:
```
>> import multiprocessing
>> cpu_count = multiprocessing.cpu_count()
>> print(cpu_count)
```

Then run this program using the following command and replacing `<FILENAME>` with the `.csv` filename, leaving out the angle brackets:
(note the $ at the beginning is to denote the command line):

`$ python aidanwebscrape.py <FILENAME>`

The files across search results for a specific provider will be gathered under a newly-generated folder with the provider as its name.

NOTE: This program took what I approximated to be an hour or two for about 250 providers in a sample .csv I ran.
I would suggest that, unless you want to run this program and babysit the computer for 40-50 hours,
you chunk out sections of the full provider list into their own `.csv` files and then run it over those.

TODO:
- Develop scraping for more general use cases
- Remove occasional errors (see `checkcrdl.py` for current stopgap)
