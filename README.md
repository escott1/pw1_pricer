# pw1_pricer
### Summary:
Analysis and npv calculator tool for a Tesla Powerwall 1 in PG&amp;E. 
<br><br>
I put this analysis together in early 2016 around the launch of the Tesla Powerwall 1. 
The objective here was to understand if purchasing a Powerwall 1 made economic sense for a 'typical' homeowner in PG&E. 
At the time (and still today) there was a lot of hype around time-of-use arbitrage with residential stationary storage. 
There are two main directories in this repo:
1. main_gui
2. write_up
#### main_gui
Contains the python scripts, csv files and images for the net-present-value (npv) calculator. In a terminal session run:<br><br>
<code>python gui.py</code><br><br>
from the main_gui directory to bring up the gui. Details below on what the different gui fields mean.
#### write_up
This was a more detailed look at the actual battery operation. See the pdf file here for the full write up, including
my approach, assumptions and details behind the battery charge / discharge algorithm.
I also put together a Powerpoint presentation that summarizes the analysis.
### Dependencies
* Python = 2.7.10
* Pandas = 0.19.1
* Numpy = 1.8.0rc1
* Seaborn
### Running the NPV GUI:
After running <code>python gui.py</code><br><br>, a screen will pop-up:
![ScreenShot](/main_gui/gui_screenshot.png)
* Select your PG&E tariff region from the drop-down menu at the top. Ex. Bay Area homes are in region 'T'
* Powerwall lifetime: select the expected life of your powerwall. Tesla's warranty is 10 years, however you can extend (or shorten this)
* Project disocunt rate: difficult to assume, can think of this like the opportunity cost rate of purchasing the PW1. For example, if money in your bank savings account is earning 2% annual interest, select 2%
* PG&E Price Escalation: is the price increase per year (in %) from PG&E. Again, difficult to assume but it does affect the NPV
* The NPV will print in the text box. You can clear the contents of the text box by pressing 'Clear'
* Close will exit the gui
