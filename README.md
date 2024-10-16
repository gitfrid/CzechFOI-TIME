# CzechFOI-TIME

## Czech FOI data analysis

A solution that makes it easy to analyse, calculate and visualise FOI data in many ways.  
Requires a certain IT affinity, but is simpler, faster and more flexible than using a spreadsheet.

The resulting 3D diagrams are interactive HTML files that can be zoomed and rotated - more analyses will follow. 
<br>You can download them from the [Plot Results Folder](https://github.com/gitfrid/CzechFOI-TIME/tree/main/Plot%20Results)

<br>**Example of an interactive 3D mesh plot of the Czech FOI data:**
<br>
_________________________________________
<br>
<img src=https://github.com/gitfrid/CzechFOI-TIME/blob/37b8e8bbc23a9949b6cb0ed07e2ecf2f689873fd/Plot%20Results/AH)%203D%20Surface%20mesh%20AGE_2023_DAYS_D_NUM_D/AH)%203D%20Surface%20mesh%20AGE_2023_DAYS_D_NUM_D.png width="600" height="auto">
<br>

<br>**Example of an interactive 3D plot**
<br>
_________________________________________
<br>
<img src="https://github.com/gitfrid/CzechFOI-TIME/blob/34c018493dfc44892c4002d602790e891eafd7f8/Plot%20Results/AH)%203d%20surface%20PVT_CUM_NUM_UVX_D/AH)%203d%20surface%20PVT_CUM_NUM_UVX_D.png" width="600" height="auto">
<br>

<br>**Example of an interactive 2D plot**
<br>
_________________________________________
<br>
<img src="https://github.com/gitfrid/CzechFOI-TIME/blob/1438e171e38ca18246cbe914efbf8c931cceed6d/Plot%20Results/AE)%202D%203Axis%201Derivat%20norm%20PVT_CUM_NUM_D_NORM%20PVT_CUM_NUM/AE)%202D%203Axis%201Derivat%20norm%20PVT_CUM_NUM_D_NORM%20PVT_CUM_NUM.png" width="600" height="auto">
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


