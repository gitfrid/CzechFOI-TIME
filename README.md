# CzechFOI-TIME

## Czech FOI data analysis

A solution that makes it easy to analyse, calculate and visualise FOI data in many ways.  
Requires a certain IT affinity, but is simpler, faster and more flexible than using a spreadsheet.

The resulting 3D diagrams are interactive HTML files that can be zoomed and rotated - more analyses will follow.
<br>To deselct all curves, double-click on a legend entry. To show a curve click onec on the legend entry. 
<br>You can download them from the [Plot Results Folder](https://github.com/gitfrid/CzechFOI-TIME/tree/main/Plot%20Results)

<br>**Example of an interactiveplot of the Czech FOI data PVT_NUM_D PVT_NUM_VD CUM NORM: 15-19**
<br>
_________________________________________
<br>
<img src=https://github.com/gitfrid/CzechFOI-TIME/blob/dfc788d553d03307d4e71cbffab2cfcf0dad01c4/Plot%20Results/AF)%202D%204Axis%20calc-cum%20pop-minus-d%20cum-d-norm%20all%20PVT_NUM_D%20PVT_NUM_VD%20CUM%20NORM/Screenshot%2015-19.png width="600" height="auto">
<br>

<br>**Example PVT_NUM_VD CUM NORM: 15-19**
<br>
_________________________________________
<br>
<img src=https://github.com/gitfrid/CzechFOI-TIME/blob/dfc788d553d03307d4e71cbffab2cfcf0dad01c4/Plot%20Results/AE)%202D%204Axis%20calc-cum%20cum-d-norm%20all%20PVT_NUM_D%20PVT_NUM_VD%20CUM%20NORM/Screenshot%2015-19.png width="600" height="auto">
<br>

<br>**Example of PVT_NUM_D PVT_NUM_VD CUM NORM: 90-94**
<br>
_________________________________________
<br>
<img src=https://github.com/gitfrid/CzechFOI-TIME/blob/dfc788d553d03307d4e71cbffab2cfcf0dad01c4/Plot%20Results/AE)%202D%204Axis%20calc-cum%20cum-d-norm%20all%20PVT_NUM_D%20PVT_NUM_VD%20CUM%20NORM/Screenshot%2090-94.png width="600" height="auto">
<br>

The original Czech FOI data, obtained through a Freedom of Information request, 
<br>The file Vesely_106_202403141131.CSV can be downloaded at [FOI Link](https://github.com/PalackyUniversity/uzis-data-analysis/blob/main/data/Vesely_106_202403141131.tar.xz)

To import view and edit the FOI data in a SQlite database, you can use **DB Browser for SQLite**.

Dates are counted as the number of days from 1 January 2020, as an integer number is easier to handle in the Python scripts than a date.
AGE_2023 stands for the age at 1 January 2023, calculated from the year of birth. Norm means that the data has been normalised per 100000 to make it comparable.

The required views were processed using the file [All SQL Queries.sql](https://github.com/gitfrid/CzechFOI-TIME/blob/main/SQLQueries/All%20SQL%20Queries.sql), 
<br>and the resulting views were manually exported to CSV files to the [TERRA folder](https://github.com/gitfrid/CzechFOI-TIME/tree/main/TERRA) 

The [Phyton Scripts](https://github.com/gitfrid/CzechFOI-TIME/tree/main/Py%20Scripts) analyse and visualise these csv data, and saves the plot result as interactive html files.

<br>**Software Download Links:**
<br>[DB Browser for SQLite 3.13.0](https://sqlitebrowser.org/dl/) to create a Database, run SQL querys and csv export.
<br>[Phyton 3.12.5](https://www.python.org/downloads/) to execute the pyton scripts ans plot the CSV data. 
<br>[Visual Studio Code 1.92.2](https://code.visualstudio.com/download) to edit and run the phyton script.

<br>**Disclaimer: The result has not been checked for errors!
<br>Neither methodological nor technical, no checks or cleansing of the raw data were carried out.** 


