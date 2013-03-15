# Purpose #
The goal of this project is to create an application that will generate strategies for selecting loans on LendingClub.com based on user constraints.

# How to use #
- Download the loan data from the Lending Club website (https://www.lendingclub.com/info/download-data.action)
- Run LC Strategy Generator.
- From the menu select CSV to build database.
 OR
- Load previously built database.
- Click generate
- Currently the selection of filters are in the generator.py and must be modified by hand.


# Log #
<b>March 14, 2013:</b>
Got a functioning tree control with checkboxes for the filters, and got it to successfully use the selected items in my generator.

<b>March 8, 2013:</b>
I had two exams this morning, so this afternoon I was finally able to work on this. I brought together some changes I started last week regarding how the algorithm processes filters. I also got a working version of the progress calculator.

<b>February 22, 2013:</b>
After getting it to work in console mode, I've been developing a UI for the app.


# To Do #
- Add UI progress bar
- Add UI for the other options in generator.py
- Fix the ROI calculation.
- Add all filter options. Currently I've only added a few filters and options, just enough to see if things work.
- Get threading to work with building database from CSV.

Done:
- Got threading to work with generator.
- Develop UI for filter options: A side panel tree structure.


# Project's Pre-History #

I began this idea in December 2012, originally writing in Java. I knew I needed a database for it, and I didn't want to wait until I took a database class, so I taught myself SQL and tried out many differ Java implementations of it. At the time, over Christmas break, I started teaching myself Python, because I saw it as a popular and versatile language. I switched the project over to Python because I was loving Python, and wanted a project outside of Java, which I was using for all my school projects.

I got this idea because I have been a lender on Lending Club since last fall. In my free time, I have studied strading financial markets (such as stocks and currencies). One of the tools I used to use when I hobbied tradding currency, was Forex Strategy Builder (forexsb.com), which has a tool for generating a trading strategy by randomly applying technical analysis indicators to a market based on the users constraints. This tool has inspired my idea for a Lending Club strategy generator.
