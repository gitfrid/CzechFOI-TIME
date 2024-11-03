import json  # Add this import at the top of your script
import pandas as pd
import plotly.graph_objects as go
import os
import shutil
from plotly.subplots import make_subplots
import numpy as np
import textwrap
import plotly.express as px
import xarray as xr
import numpy as np


def main():

    # set plot titele and the filename depending on choosed vars
    plt = {   
        "title_text": "Rolling cross correlation",         
        "window_size_correl": 50,
        "window_size_mov_average": 14,
        "max_lag": 1500,  # Maximum lag (both positive and negative)
        "normalize": True,
        "normalize_cumulate_deaths": True,
        "population_minus_death": True,
        "correl_data_series" : ""        
    } 

    pairs = [
            ('Avg NUM_DVX','Avg NUM_VDA'),
            ('Avg NUM_DUVX','Avg NUM_VDA'),
            ('Avg NUM_D','Avg NUM_VDA')
    ]
    
    csv_files_dvd = [
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_D.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DUVX.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVX.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVD1.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVD2.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVD3.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVD4.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVD5.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVD6.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVD7.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_DVDA.csv",
    ]
    csv_files_vd = [
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_POP.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_UVX.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VX.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VD1.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VD2.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VD3.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VD4.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VD5.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VD6.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VD7.csv",
        r"C:\Github\CzechFOI-TIME\TERRA\PVT_NUM_VDA.csv",
    ]
  
    # Initialize plot name - title - axis text
    plo = init_plot_title(plt, pairs)

    csv_files_cum_dvd = [
        os.path.join(os.path.dirname(file), os.path.basename(file).replace("PVT_", "PVT_CUM_"))
        for file in csv_files_dvd
    ]
    csv_files_cum_vd = [
        os.path.join(os.path.dirname(file), os.path.basename(file).replace("PVT_", "PVT_CUM_"))
        for file in csv_files_vd
    ]
    dataframes_dvd = [pd.read_csv(file) for file in csv_files_dvd]
    dataframes_vd = [pd.read_csv(file) for file in csv_files_vd]
    age_bands = dataframes_dvd[0].columns[1:]
    
    cumulative_dataframes_dvd = []
    for df in dataframes_dvd:
        df_cumulative_dvd = df.copy()
        df_cumulative_dvd[age_bands] = df[age_bands].cumsum()
        cumulative_dataframes_dvd.append(df_cumulative_dvd)

    # calcualte cumulating values - subtract deaths if population_minus_death is true 
    cumulative_dataframes_vd = []    
    for i, df in enumerate(dataframes_vd):
        df_cumulative_vd = df.copy()
        if i == 0:
            if plt["population_minus_death"] :
                df_cumulative_vd[age_bands] = dataframes_vd[0][age_bands] - dataframes_dvd[0][age_bands].cumsum()
            else :
                df_cumulative_vd[age_bands] = dataframes_vd[0][age_bands]                
        elif i == 1:
            if plt["population_minus_death"] :
                df_cumulative_vd[age_bands] = dataframes_vd[0][age_bands] + df[age_bands].cumsum() - cumulative_dataframes_dvd[1][age_bands]
            else :
                df_cumulative_vd[age_bands] = dataframes_vd[0][age_bands] + df[age_bands].cumsum() 
        else:
            if plt["population_minus_death"] :
                df_cumulative_vd[age_bands] = df[age_bands].cumsum() - cumulative_dataframes_dvd[i][age_bands]
            else :
                df_cumulative_vd[age_bands] = df[age_bands].cumsum()
        cumulative_dataframes_vd.append(df_cumulative_vd)

    # save to csv files adding PVT_CUM_ to filename   
    for cum_df, output_file in zip(cumulative_dataframes_dvd, csv_files_cum_dvd):
        cum_df.to_csv(output_file, index=False)
    for cum_df, output_file in zip(cumulative_dataframes_vd, csv_files_cum_vd):
        cum_df.to_csv(output_file, index=False)
    
    # Initialize the directory and copy py script
    full_plotfile_name = init_function(f"{plo["name"]} {plo["pairs_text"]}")
    
    # Deaths normalized and then cumulated or not
    if plt["normalize_cumulate_deaths"] == True :
        cum_dataframes_dvd = []
        for i, df in enumerate(dataframes_dvd):
            df_cum_dvd = df.copy()
            df_cum_dvd[age_bands] = (dataframes_dvd[i][age_bands] / cumulative_dataframes_vd[i][age_bands]) * 100000
            cum_dataframes_dvd.append(df_cum_dvd)
        cumulat_dataframes_dvd = []
        for df in cum_dataframes_dvd:
            df_cumulat_dvd = df.copy()
            df_cumulat_dvd[age_bands] = df[age_bands].cumsum()
            cumulat_dataframes_dvd.append(df_cumulat_dvd)
    else:
        cum_dataframes_dvd = []
        for i, df in enumerate(dataframes_dvd):
            df_cum_dvd = df.copy()
            df_cum_dvd[age_bands] = dataframes_dvd[i][age_bands]
            cum_dataframes_dvd.append(df_cum_dvd)
        cumulat_dataframes_dvd = []
        for df in cum_dataframes_dvd:
            df_cumulat_dvd = df.copy()
            df_cumulat_dvd[age_bands] = df[age_bands].cumsum()
            cumulat_dataframes_dvd.append(df_cumulat_dvd)    
    
    # Normalize the data per 100,000 
    if plt["normalize"] == True :
        for i in range(0, len(dataframes_dvd)):
            for age_band in age_bands:
                dataframes_dvd[i][age_band] = (dataframes_dvd[i][age_band] / cumulative_dataframes_vd[i][age_band]) * 100000
        
    # Helper function cross-correlation to filter out zero values and align lengths
    def filter_and_align(series1, series2):
        non_zero_1 = series1[series1 != 0]
        non_zero_2 = series2[series2 != 0]
        min_length = min(len(non_zero_1), len(non_zero_2))
        return non_zero_1[:min_length], non_zero_2[:min_length]

    def first_nonzero_index(series):
        non_zero_indices = np.nonzero(series)[0]
        if len(non_zero_indices) > 0:
            return non_zero_indices[0]
        else:
            return None  # Handle this case as needed

    def calculate_cross_correlation(series1, series2, max_lag):
        # Prepare lags array
        lags = np.arange(-max_lag, max_lag + 1)
        ccf_results = xr.DataArray(np.zeros(lags.shape), coords=[lags], dims=['lag'])

        for i, lag in enumerate(lags):
            # Shift series2 according to lag, with zero fill to handle edges
            shifted_series2 = series2.shift(time=abs(lag), fill_value=0) if lag != 0 else series2
            
            # Use correlation calculation for each lag without pre-normalizing entire series
            if lag < 0:
                shifted_series2 = shifted_series2.roll(time=lag)  # Align for negative lags
            else:
                shifted_series2 = shifted_series2.roll(time=lag)
                
            # Calculate correlation, ignoring NaNs
            ccf_results[i] = xr.corr(series1, shifted_series2, dim='time')

        return ccf_results

    
    def first_nonzero_index(series):
        print("Series content:", series)  # Debugging: Print the series to check its content
        if isinstance(series, xr.DataArray):
            series = series.values  # Convert to NumPy array for processing
        non_zero_indices = np.nonzero(series)[0]
        if len(non_zero_indices) > 0:
            return non_zero_indices[0]
        else:
            return None  # Or handle this case as needed
        
    # Choose a color palette with many colors
    color_palette = px.colors.qualitative.Dark24

    # Create a plot for each age band
    for age_band in age_bands:                   
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces for each dataframe (CSV-file)
        for i in range(0, len(dataframes_dvd)):
           
            # Add traces for DVD on primary y-axis
            fig.add_trace(go.Scatter(
                x=dataframes_dvd[i].iloc[:, 0],
                y=dataframes_dvd[i][age_band],
                mode='lines',
                line=dict(dash='solid', color=color_palette[i % len(color_palette)]),
                name=os.path.splitext(os.path.basename(csv_files_dvd[i]))[0][4:]
            ), secondary_y=False)

            # Calculate add moving average for DVD
            moving_average_dvd = dataframes_dvd[i][age_band].rolling(window=plt["window_size_mov_average"]).mean()
            fig.add_trace(go.Scatter(
                x=dataframes_dvd[i].iloc[:, 0],
                y=moving_average_dvd,
                mode='lines',
                line=dict(dash='solid', width=1, color=color_palette[i % len(color_palette)]),
                name=f'Avg {os.path.splitext(os.path.basename(csv_files_dvd[i]))[0][4:]}',
                showlegend=True
            ), secondary_y=False)

            # Add trace for VD
            fig.add_trace(go.Scatter(
                x=dataframes_vd[i].iloc[:, 0],
                y=dataframes_vd[i][age_band],
                mode='lines',
                line=dict(dash='dot', color=color_palette[i % len(color_palette)]),
                name=os.path.splitext(os.path.basename(csv_files_vd[i]))[0][4:]
            ), secondary_y=False)            
            
            # Calculate add moving average for VD
            moving_average_vd = dataframes_vd[i][age_band].rolling(window=plt["window_size_mov_average"]).mean()
            fig.add_trace(go.Scatter(
                x=dataframes_vd[i].iloc[:, 0],
                y=moving_average_vd,
                mode='lines',
                line=dict(dash='solid', width=1, color=color_palette[i % len(color_palette)]),
                name=f'Avg {os.path.splitext(os.path.basename(csv_files_vd[i]))[0][4:]}',
                showlegend=True
            ), secondary_y=False)

            # Add cumulative DVD data traces on the secondary y-axis
            fig.add_trace(go.Scatter(
                x=cumulat_dataframes_dvd[i].iloc[:, 0],
                y=cumulat_dataframes_dvd[i][age_band],
                mode='lines',
                line=dict(dash='solid', color=color_palette[i % len(color_palette)]),
                name=f'cum {os.path.splitext(os.path.basename(csv_files_dvd[i]))[0][4:]}'
            ), secondary_y=True)

            # Add cumulative VD data traces on the secondary y-axis
            fig.add_trace(go.Scatter(
                x=cumulative_dataframes_vd[i].iloc[:, 0],
                y=cumulative_dataframes_vd[i][age_band],
                mode='lines',
                line=dict(dash='dot', color=color_palette[i % len(color_palette)]),
                name=f'cum {os.path.splitext(os.path.basename(csv_files_vd[i]))[0][4:]}'
            ), secondary_y=True)

        # Define colors for 3 rolling correlation curves 
        colors = ['orangered', 'yellowgreen', 'deepskyblue']  

        # Extract moving averages from the traces
        moving_averages = {trace.name: xr.DataArray(trace.y, dims='time', coords={'time': np.arange(len(trace.y))}) for trace in fig.data}

        # calculate cross correlation CCF for moving averages of the 3  Dataseries pairs
        # Extract moving averages from the traces
        # moving_averages = {trace.name: trace.y for trace in fig.data if 'Avg' in trace.name}

        # Use the moving averages for the CCF calculation
        for i, (name1, name2) in enumerate(pairs):
            try:
                moving_avg_df1 = moving_averages[name1]
                moving_avg_df2 = moving_averages[name2]
            except KeyError as e:
                print(f"KeyError: {e} not found in moving_averages")
                continue

            # Filter and align the moving averages
            filtered_df1, filtered_df2 = filter_and_align(moving_avg_df1, moving_avg_df2)

            # Ensure filtered data is not empty and is 1D
            if filtered_df1.size == 0 or filtered_df2.size == 0:
                print("One of the filtered arrays is empty. Skipping this pair.")
                continue  # Skip further processing for this pair

            # Ensure arrays are 1D
            if np.isscalar(filtered_df1):
                filtered_df1 = np.array([filtered_df1])
            if np.isscalar(filtered_df2):
                filtered_df2 = np.array([filtered_df2])

            print("Filtered DF1 shape:", filtered_df1.shape)
            print("Filtered DF2 shape:", filtered_df2.shape)

            start_idx1 = first_nonzero_index(filtered_df1)
            start_idx2 = first_nonzero_index(filtered_df2)
            start_idx = max(start_idx1 or 0, start_idx2 or 0)

            # Trim arrays to start from the first non-zero index, if valid
            if start_idx < len(filtered_df1) and start_idx < len(filtered_df2):
                filtered_df1 = filtered_df1[start_idx:]
                filtered_df2 = filtered_df2[start_idx:]

            # Remove NaN values
            filtered_df1 = filtered_df1[~np.isnan(filtered_df1)]
            filtered_df2 = filtered_df2[~np.isnan(filtered_df2)]

            # Ensure they are of equal length
            min_length = min(len(filtered_df1), len(filtered_df2))
            filtered_df1 = filtered_df1[:min_length]
            filtered_df2 = filtered_df2[:min_length]

            if len(filtered_df1) > 0 and len(filtered_df2) > 0:
                # Convert to xarray DataArrays
                moving_avg_df1 = xr.DataArray(filtered_df1, dims='time', coords={'time': np.arange(len(filtered_df1))})
                moving_avg_df2 = xr.DataArray(filtered_df2, dims='time', coords={'time': np.arange(len(filtered_df2))})

                # Calculate cross-correlation
                cross_corr = calculate_cross_correlation(moving_avg_df1, moving_avg_df2, plt["max_lag"])

                # Prepare x-values for plotting
                x_values = cross_corr['lag'].values  # Using lag as x-values
                y_values = cross_corr.values  # CCF values for plotting

                # Add the trace for the cross-correlation
                fig.add_trace(go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode='lines',
                    name=f'CCF {name1}<br>{name2}',
                    line=dict(dash='solid', width=1, color=colors[i % len(colors)]),
                    xaxis=f'x{i+1}',  # Assign independent x-axes
                ), secondary_y=True)

                    
        
        # Update plot layout for dual y-axes 
        plo["age_band"] = age_band       
        fig.update_layout(
            colorway=color_palette,
            title=dict( 
                text = f'{plo["title_text"]} AGE: {age_band}<br><br><sup>{plo["subtitle_text"]}</sup>',
                y=0.97, 
                font=dict(size=18),
                x=0.2, 
                xanchor='center', 
                yanchor='top'
            ),
            xaxis=dict(title='Lag Days'),
            yaxis=dict(
                title=plo["yaxis1_title"],
                side='left'
            ),
            yaxis2=dict(
                title=f'Values y2 VD',
                anchor='free',
                position=0.05,
                side='left'
            ),
            yaxis3=dict(
                title=plo["yaxis3_title"],
                overlaying="y",
                side="right",
                position=0.9
            ),
            yaxis4=dict(
                title=f'Cumulative Values y4 VD',
                overlaying="y",
                side="right"
            ),
            yaxis5=dict(
                title=f'Rolling correlation (CCF) y5',
                overlaying="y",
                side="right",
                position=0.8
            ),   
            legend=dict(
                orientation="v",
                xanchor="left",
                x=1.05,
                yanchor="top",
                y=1,
                font=dict(size=10)
            ),
            margin=dict(l=40, r=50, t=40, b=40)
        )

        # update trace assignment to the y-axes
        # minus the three additional CCF correlation traces
        for j in range(len(fig.data) - 3):
            if j % 6 == 0 or j % 6 == 1:
                fig.data[j].update(yaxis='y1')
            elif j % 6 == 2 or j % 6 == 3:
                fig.data[j].update(yaxis='y2')
            elif j % 6 == 4:
                fig.data[j].update(yaxis='y3')
            elif j % 6 == 5:
                fig.data[j].update(yaxis='y4')

        # Assignment of the curves for CCF correlation 1-3
        # on the same axis to obtain the same scale
        fig.data[len(fig.data)-1].update(yaxis='y5')
        fig.data[len(fig.data)-2].update(yaxis='y5')
        fig.data[len(fig.data)-3].update(yaxis='y5')

        # Save the plot to an HTML file
        #fig.write_html(f"{full_plotfile_name} AG_{age_band}.html")
        #print(f"Plot {full_plotfile_name} {age_band} has been saved to HTML file.")

        # Save the plot to an HTML file with a custom legend
        html_file_path = f"{full_plotfile_name} AG_{age_band}.html"

        # Prepare custom legend items based on the figure traces
        legend_items = []
        for trace in fig['data']:
            legend_items.append({
                'name': trace['name'] if 'name' in trace else 'Unnamed Trace',
                'color': trace['line']['color'] if 'line' in trace and 'color' in trace['line'] else '#000000'  # Default color if not set
            })

        # Set the desired height and width (in pixels)
        desired_height = 800  # Adjust this value as needed
        desired_width = 2096  # Adjust this value as needed

        # Create the complete HTML
        with open(html_file_path, 'w') as f:
            f.write('<!DOCTYPE html>\n<html lang="de">\n<head>\n')
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write('    <title>Plotly Diagramm mit großer Tabellenlegende</title>\n')
            f.write('    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')
            f.write('    <style>\n')
            f.write('        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }\n')
            f.write('        #legend { display: grid; grid-template-columns: repeat(6, 1fr); gap: 5px; margin-top: 20px; }\n')
            f.write('        .legend-item { display: flex; align-items: center; cursor: pointer; font-size: 12px; }\n')  # Smaller font size
            f.write('        .legend-color-box { width: 10px; height: 10px; margin-right: 5px; }\n')  # Smaller color box
            f.write('    </style>\n')
            f.write('</head>\n<body>\n')
            f.write('    <div id="plotly-figure" style="width: ' + str(desired_width) + "px; height: " + str(desired_height) + 'px;"></div>\n')
            f.write('    <div id="legend"></div>\n')
            f.write('    <script>\n')

            # Insert the Plotly figure data
            fig_json = fig.to_json()  # Get the JSON string
            fig_data = json.loads(fig_json)  # Convert it to a dictionary
            f.write('    var data = ' + json.dumps(fig_data['data']) + ';\n')  # Access and write the data

            # Enable default legend
            layout = fig_data['layout']
            layout['showlegend'] = True  # Ensure the default legend is visible
            f.write('    var layout = ' + json.dumps(layout) + ';\n')  # Use json.dumps for layout
            f.write('    Plotly.newPlot("plotly-figure", data, layout);\n')

            # Add custom legend items to the script
            f.write('    var legendItems = ' + json.dumps(legend_items) + ';\n')
            f.write('    console.log("Legend Items:", legendItems); // Debugging line\n')  # Debugging output
            f.write('    var legendDiv = document.getElementById("legend");\n')
            
            # Track the state of all traces
            f.write('    var allVisible = true;\n')  # State to track if all traces are visible

            f.write('    legendItems.forEach(function(item, index) {\n')
            f.write('        var legendItem = document.createElement("div");\n')
            f.write('        legendItem.className = "legend-item";\n')
            
            # Set initial visibility based on data
            f.write('        var traceVisible = data[index].visible !== false;\n')
            f.write('        legendItem.innerHTML = `<div class="legend-color-box" style="background-color: ${item.color}; opacity: ${traceVisible ? 1 : 0.5};"></div>${item.name}`;\n')
            f.write('        legendItem.style.color = traceVisible ? "black" : "gray";\n')

            # Add click event listener for individual trace toggle
            f.write('        legendItem.onclick = function() {\n')
            f.write('            var currentVisibility = data[index].visible;\n')
            f.write('            // Toggle the visibility\n')
            f.write('            data[index].visible = (currentVisibility === true || currentVisibility === "true") ? false : true;\n')

            # Update the legend item appearance based on visibility
            f.write('            if (data[index].visible) {\n')
            f.write('                legendItem.querySelector(".legend-color-box").style.opacity = "1";\n')
            f.write('                legendItem.style.color = "black";\n')
            f.write('            } else {\n')
            f.write('                legendItem.querySelector(".legend-color-box").style.opacity = "0.5";\n')
            f.write('                legendItem.style.color = "gray";\n')
            f.write('            }\n')

            # Use Plotly.react for a more efficient update
            f.write('            Plotly.react("plotly-figure", data, layout);\n')
            f.write('        };\n')

            # Add double-click event listener for select/deselect all
            f.write('        legendItem.ondblclick = function() {\n')
            f.write('            allVisible = !allVisible;\n')  # Toggle the visibility state
            f.write('            data.forEach(function(trace) {\n')
            f.write('                trace.visible = allVisible;  // Set all traces to the same visibility state\n')
            f.write('            });\n')
            f.write('            Plotly.update("plotly-figure", data, layout);  // Update the plot\n')

            # Update all legend items based on the visibility state
            f.write('            var newOpacity = allVisible ? 1 : 0.5;\n')
            f.write('            var newColor = allVisible ? "black" : "gray";\n')
            f.write('            var legendItems = document.querySelectorAll(".legend-item");\n')
            f.write('            legendItems.forEach(function(item) {\n')
            f.write('                item.querySelector(".legend-color-box").style.opacity = newOpacity;\n')
            f.write('                item.style.color = newColor;\n')
            f.write('            });\n')  # Update all legend items
            f.write('        };\n')

            # Append the legend item to the legend div
            f.write('        legendDiv.appendChild(legendItem);\n')
            f.write('    });\n')
            f.write('</script>\n')
            f.write('</body>\n</html>\n')

        print(f"Plot {full_plotfile_name} {age_band} has been saved to HTML file.")



# Initialize the plot name - plot title text - axis text
def init_plot_title(plt,pairs):        
    # generate plot name
    plot_name = f"AVG_{plt["window_size_mov_average"]} CORR_{plt["window_size_correl"]} LAG_{plt["max_lag"]}"
    if plt["normalize"] == True : plot_name = f"N {plot_name}"
    if plt["normalize_cumulate_deaths"] : plot_name = f"N-CUM-D {plot_name}"        
    if plt["population_minus_death"] : plot_name = f"POP-D {plot_name}"
    plot_name = f"{plot_name}"
    print ( f"pltname: { plot_name }")    
    # plot title_text 
    title_text = plt["title_text"]        
    # generate pairs_text 
    pairs_text = ""
    for pair in pairs:
        pairs_text = f"{pairs_text} {pair[0].replace(" ", "").replace("Avg", "A")}-{pair[1].replace(" ", "").replace("Avg", "A")}"        
    pairs_text = pairs_text.lstrip()
    # generate subtitle text and axis text depending on choosed vars        
    subtitle_text = f"{''.join(textwrap.wrap(plot_name, 45, break_long_words=False, replace_whitespace=False))}<br>"    
    subtitle_text = f"{subtitle_text}{pairs_text}<br>"    
    if plt["normalize"] == True : 
        subtitle_text = f'{subtitle_text}Values were normalized per 100000<br>'
        yaxis1_title=f'Values per 100000 y1 DVD'            
    else:
        yaxis1_title=f'Values y1 DVD'
    if plt["normalize_cumulate_deaths"] :
        subtitle_text = f'{subtitle_text}The cumulative deaths were first normalized and then cumulated.<br>'      
        yaxis3_title=f"Values per 100000 Cumulative y3 DVD"
    else :
        yaxis3_title=f"Values Cumulative y3 DVD"
    if plt["population_minus_death"] :
        subtitle_text = f'{subtitle_text}Deaths were subtracted from population, X-axis Date - days from 2020-01-01<br>'           
    else :
        subtitle_text = f'{subtitle_text}Deaths not! subtracted from population<br>'
    subtitle_text = f'{subtitle_text}To deselect all - double-click on a legend entry'
    return {"name": plot_name,
            "pairs_text": pairs_text,
            "title_text": title_text,
            "subtitle_text": subtitle_text,
            "yaxis1_title": yaxis1_title,
            "yaxis3_title": yaxis3_title}
    

# Initialize the "Plot Results" directory and copy this PyScript into it
def init_function(plt_name):
    print (plt_name)
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    first_root_dir = os.path.abspath(os.sep.join(script_dir.split(os.sep)[:2]))
    plot_result_path = os.path.join(first_root_dir, "Plot Results", f"{script_name} {plt_name}")
    os.makedirs(plot_result_path, exist_ok=True)
    
    script_file_name = os.path.join(plot_result_path, f"{script_name}.py")
    if not os.path.exists(script_file_name):
        shutil.copy(__file__, script_file_name)
    # return plot file name without extension
    return plot_result_path + os.sep + f"{script_name} {plt_name}"

# call main script
if __name__ == "__main__": main()
