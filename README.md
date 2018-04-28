# browser-history-analyzer

Introduction
=============
This Repo is the project of CS 498 AL1: Digital forensics. Browser history analyzer is a 
very simple to use and convinient tool to analyze the browser history on disk. This tool
can analyze the three mainstream browsers: Chrome, Firefox, Safari. This software can 
find all the browsing history related files from the filesystem or any recovered image 
and can analyze browsing history and related information. We can use specific configuration
for displaying or choosing a time frame to filter the analysis for investigation and even show
the statistics. It will generate csv files for history and statistics and a jpg file for the pie
chart of statistics.

Usage
=============
To make it simple to use, I want to get rid of the complicated commandline argument.
All we need to do is by modifying configuration.config to make the tool perform the
way we want.

Usage: ``python anazlyze.py``

Explanation of configuration
=============
1. Browser: the browser we want to explore. (``chrome``, ``safari``, ``firefox`` supported)
2. Path: the path we want to search for browser history. (Please use ``~`` as default)
3. Statistics: to show the statistics or not. (``true`` of ``false``)
4. Plot: to draw the pie chart of the statistics or not. (``true`` of ``false``)
5. Plot number: the number we want to show on the pie chart.
6. History list: to show the list of history or not. (``true`` of ``false``)
7. Start time: the start time stamp filter. (``yy-mm-dd`` or ``yy-mm-dd HH-MM-SS``)
8. End time: Then end time stamp filter. (``yy-mm-dd`` or ``yy-mm-dd HH-MM-SS``)
9. Keyword: The keywords for the filter.

Packages
=============
All packages required are in requirement.txt. Please run ``pip install -r requirement.txt``