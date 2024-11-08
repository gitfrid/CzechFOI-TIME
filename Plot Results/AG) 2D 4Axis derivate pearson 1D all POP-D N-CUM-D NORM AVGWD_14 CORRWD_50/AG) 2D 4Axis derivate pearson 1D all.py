import json  
import pandas as pd
import plotly.graph_objects as go
import os
import shutil
from plotly.subplots import make_subplots
import numpy as np
import textwrap
import numpy as np
import plotly.graph_objects as go
from matplotlib import colors as mcolors 
import colorsys
import plotly.express as px


def main():

    # set plot titele and the filename depending on choosed vars
    plt = {   
        "title_text": "rolling perason for 1st Derivate",         
        "window_size_correl": 50,
        "window_size_mov_average": 14,
        "normalize": True,
        "normalize_cumulate_deaths": True,
        "population_minus_death": True,
        "correl_data_series" : ""
    } 

       
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
  
    pairs = [
        ('Avg 1D NUM_D', 'Avg 1D NUM_DUVX'),
        ('Avg 1D NUM_D', 'Avg 1D NUM_DVX'),
        ('Avg 1D NUM_D', 'Avg 1D NUM_DVD1'),
        ('Avg 1D NUM_D', 'Avg 1D NUM_DVD2'),
        ('Avg 1D NUM_D', 'Avg 1D NUM_DVDA'),       
        ('Avg 1D NUM_D', 'Avg 1D NUM_UVX'),
        ('Avg 1D NUM_D', 'Avg 1D NUM_VX'),
        ('Avg 1D NUM_D', 'Avg 1D NUM_VD1'),
        ('Avg 1D NUM_D', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_D', 'Avg 1D NUM_VDA'),
        
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_DVX'),
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_DVD1'),
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_DVD2'),
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_DVDA'),
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_UVX'),
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_VX'),
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_VD1'),
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_DUVX', 'Avg 1D NUM_VDA'),
        
        ('Avg 1D NUM_DVX', 'Avg 1D NUM_DVD1'),
        ('Avg 1D NUM_DVX', 'Avg 1D NUM_DVD2'),
        ('Avg 1D NUM_DVX', 'Avg 1D NUM_DVDA'),
        ('Avg 1D NUM_DVX', 'Avg 1D NUM_UVX'),
        ('Avg 1D NUM_DVX', 'Avg 1D NUM_VX'),
        ('Avg 1D NUM_DVX', 'Avg 1D NUM_VD1'),
        ('Avg 1D NUM_DVX', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_DVX', 'Avg 1D NUM_VDA'),
        
        ('Avg 1D NUM_DVD1', 'Avg 1D NUM_DVD2'),
        ('Avg 1D NUM_DVD1', 'Avg 1D NUM_DVDA'),
        ('Avg 1D NUM_DVD1', 'Avg 1D NUM_UVX'),
        ('Avg 1D NUM_DVD1', 'Avg 1D NUM_VX'),
        ('Avg 1D NUM_DVD1', 'Avg 1D NUM_VD1'),
        ('Avg 1D NUM_DVD1', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_DVD1', 'Avg 1D NUM_VDA'),
        
        ('Avg 1D NUM_DVD2', 'Avg 1D NUM_DVDA'),
        ('Avg 1D NUM_DVD2', 'Avg 1D NUM_UVX'),
        ('Avg 1D NUM_DVD2', 'Avg 1D NUM_VX'),
        ('Avg 1D NUM_DVD2', 'Avg 1D NUM_VD1'),
        ('Avg 1D NUM_DVD2', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_DVD2', 'Avg 1D NUM_VDA'),
        
        ('Avg 1D NUM_DVDA', 'Avg 1D NUM_UVX'),
        ('Avg 1D NUM_DVDA', 'Avg 1D NUM_VX'),
        ('Avg 1D NUM_DVDA', 'Avg 1D NUM_VD1'),
        ('Avg 1D NUM_DVDA', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_DVDA', 'Avg 1D NUM_VDA'),
        
        
        ('Avg 1D NUM_UVX', 'Avg 1D NUM_VX'),
        ('Avg 1D NUM_UVX', 'Avg 1D NUM_VD1'),
        ('Avg 1D NUM_UVX', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_UVX', 'Avg 1D NUM_VDA'),
        
        ('Avg 1D NUM_VX', 'Avg 1D NUM_VD1'),
        ('Avg 1D NUM_VX', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_VX', 'Avg 1D NUM_VDA'),
        
        ('Avg 1D NUM_VD1', 'Avg 1D NUM_VD2'),
        ('Avg 1D NUM_VD1', 'Avg 1D NUM_VDA'),
        
        ('Avg 1D NUM_VD2', 'Avg 1D NUM_VDA')
    ]
    
    # Initialize plot names and parameters
    plo = init_plot_title(plt)

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
    #full_plotfile_name = init_function(f"{plo["name"]} {plo["pairs_text"]}")
    full_plotfile_name = init_function(f"{plo["name"]}")
    
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


    # Define a color palette from Plotly (you can use any available palette)
    # color_palette = px.colors.qualitative.dark24 

    # Custom color palette (11 color pairs)
    color_palette = [
        '#174a75', '#990099', '#9a1f1e', '#47327f', '#1f6024', '#804d1b',
        '#5d4a00', '#716c0f', '#4e4059', '#af9f66', '#505b9f', '#9f3e0e',
        '#5e7775', '#43472d', '#b9ae92', '#9c542b', '#5a5034', '#1f738b',
        '#4c6d1e', '#e1b5e4', '#73666a', '#9e8d39'
    ]

    # Function for creating shades (reusable for each color palette)
    def generate_shades(base_color, num_shades=5, lightness_factor=0.1):
        shades = []
        # Convert hex color to RGB
        if base_color.startswith("#"):            
            base_color = mcolors.to_rgb(base_color)

        # Convert RGB to HSV (hue, saturation, brightness)
        hsv = colorsys.rgb_to_hsv(base_color[0], base_color[1], base_color[2])

        # Create shades by varying the brightness
        for i in range(num_shades):
            new_value = min(1.0, max(0.4, hsv[2] + lightness_factor * (i - 2)))  # Adjust brightness
            new_rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], new_value)  # Keep hue and saturation constant
            new_hex = mcolors.rgb2hex(new_rgb)  # Convert back to Hex
            shades.append(new_hex)

        return shades

    # Function for creating color pairs and shades
    def generate_color_shades(color_palette, n_pairs=11):
        color_shades = {}
        for i in range(n_pairs):
            # Select color pairs from the palette
            base_color_dvd_1 = color_palette[i % len(color_palette)]
            base_color_vd_1 = color_palette[(i + 1) % len(color_palette)]

            # Calculate shading for the DVD and VD
            shades_dvd_1 = generate_shades(base_color_dvd_1)
            shades_vd_1 = generate_shades(base_color_vd_1)

            # Save the shades
            color_shades[i] = (shades_dvd_1, shades_vd_1)

        return color_shades

    # Generate shades for all color pairs
    color_shades = generate_color_shades(color_palette, n_pairs=11)

    # Create a plot for each age band
    for age_band in age_bands:                   
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces for each dataframe (CSV-file)
        for i in range(0, len(dataframes_dvd)):
            # Get the color shades for the current dataset (ensure the shades list is long enough)
            shades_1, shades_2 = color_shades[i]

            # Add traces for DVD on primary y-axis
            fig.add_trace(go.Scatter(
                x=dataframes_dvd[i].iloc[:, 0],
                y=dataframes_dvd[i][age_band],
                mode='lines',
                line=dict(dash='solid', color=shades_1[0 % len(shades_1)]),
                name=os.path.splitext(os.path.basename(csv_files_dvd[i]))[0][4:]
            ), secondary_y=False)

            # Calculate add moving average for DVD
            moving_average_dvd = dataframes_dvd[i][age_band].rolling(window=plt["window_size_mov_average"]).mean()
            # Calculate the first derivative (approximate as the difference between consecutive moving averages)
            first_derivative_dvd = moving_average_dvd.diff()
            # Calculate the second derivative (difference between consecutive first derivatives)
            second_derivative_dvd = first_derivative_dvd.diff()
            
            # Add trace for the moving average
            fig.add_trace(go.Scatter(
                x=dataframes_dvd[i].iloc[:, 0],
                y=moving_average_dvd,
                mode='lines',
                line=dict(dash='solid', width=1, color=shades_1[1 % len(shades_1)]),
                name=f'Avg {os.path.splitext(os.path.basename(csv_files_dvd[i]))[0][4:]}',
                showlegend=True
            ), secondary_y=False)

            # Add trace for the moving average of the first derivative
            fig.add_trace(go.Scatter(
                x=dataframes_dvd[i].iloc[:, 0],
                y=first_derivative_dvd.rolling(window=plt["window_size_mov_average"]).mean(),
                mode='lines',
                line=dict(dash='dash', width=1, color=shades_1[2 % len(shades_1)]),
                name=f'Avg 1D {os.path.splitext(os.path.basename(csv_files_dvd[i]))[0][4:]}',
                showlegend=True
            ), secondary_y=True)  # You can choose secondary_y=True if needed for scaling

            # Add trace for the moving average of the second derivative
            fig.add_trace(go.Scatter(
                x=dataframes_dvd[i].iloc[:, 0],
                y=second_derivative_dvd.rolling(window=plt["window_size_mov_average"]).mean(),
                mode='lines',
                line=dict(dash='dot', width=1, color=shades_1[3 % len(shades_1)]),
                name=f'Avg 2D {os.path.splitext(os.path.basename(csv_files_dvd[i]))[0][4:]}',
                showlegend=True
            ), secondary_y=True)

            # Add cumulative DVD data traces on the secondary y-axis
            fig.add_trace(go.Scatter(
                x=cumulat_dataframes_dvd[i].iloc[:, 0],
                y=cumulat_dataframes_dvd[i][age_band],
                mode='lines',
                line=dict(dash='solid', color=shades_1[4 % len(shades_1)]),
                name=f'cum {os.path.splitext(os.path.basename(csv_files_dvd[i]))[0][4:]}'
            ), secondary_y=True)

            # Add trace for VD
            fig.add_trace(go.Scatter(
                x=dataframes_vd[i].iloc[:, 0],
                y=dataframes_vd[i][age_band],
                mode='lines',
                line=dict(dash='dot', color=shades_2[0 % len(shades_2)]),
                name=os.path.splitext(os.path.basename(csv_files_vd[i]))[0][4:]
            ), secondary_y=False)            
            
            # Calculate add moving average for VD
            moving_average_vd = dataframes_vd[i][age_band].rolling(window=plt["window_size_mov_average"]).mean()
            # Calculate the first derivative (approximate as the difference between consecutive moving averages)
            first_derivative_vd = moving_average_vd.diff()
            # Calculate the second derivative (difference between consecutive first derivatives)
            second_derivative_vd = first_derivative_vd.diff()
            
            # Add trace for the moving average
            fig.add_trace(go.Scatter(
                x=dataframes_vd[i].iloc[:, 0],
                y=moving_average_vd,
                mode='lines',
                line=dict(dash='solid', width=1, color=shades_2[1 % len(shades_2)]),
                name=f'Avg {os.path.splitext(os.path.basename(csv_files_vd[i]))[0][4:]}',
                showlegend=True
            ), secondary_y=False)

            # Add trace for the moving average of the first derivative
            fig.add_trace(go.Scatter(
                x=dataframes_vd[i].iloc[:, 0],
                y=first_derivative_vd.rolling(window=plt["window_size_mov_average"]).mean(),
                mode='lines',
                line=dict(dash='dash', width=1, color=shades_2[2 % len(shades_2)]),
                name=f'Avg 1D {os.path.splitext(os.path.basename(csv_files_vd[i]))[0][4:]}',
                showlegend=True
            ), secondary_y=True)  

            # Add trace for the moving average of the second derivative
            fig.add_trace(go.Scatter(
                x=dataframes_vd[i].iloc[:, 0],
                y=second_derivative_vd.rolling(window=plt["window_size_mov_average"]).mean(),
                mode='lines',
                line=dict(dash='dot', width=1, color=shades_2[3 % len(shades_2)]),
                name=f'Avg 2D {os.path.splitext(os.path.basename(csv_files_vd[i]))[0][4:]}',
                showlegend=True
            ), secondary_y=True)

            # Add cumulative VD data traces on the secondary y-axis
            fig.add_trace(go.Scatter(
                x=cumulative_dataframes_vd[i].iloc[:, 0],
                y=cumulative_dataframes_vd[i][age_band],
                mode='lines',
                line=dict(dash='dot', color=shades_2[4 % len(shades_2)]),
                name=f'cum {os.path.splitext(os.path.basename(csv_files_vd[i]))[0][4:]}'
            ), secondary_y=True)

        # Define colors for rolling correlation curves 
        # colors = ['orangered', 'yellowgreen', 'deepskyblue']  
        # Use Plotly's built-in 'Plotly' color palette (it has 24 distinct colors)
        color_palette = px.colors.qualitative.Plotly 

        # Extract data from the traces
        data = {trace.name: trace.y for trace in fig.data}
        
        # Function to calculate rolling correlation using the derivatives
        def rolling_correlation(series1, series2, window_size_correl):
            correl_values = []
            for i in range(len(series1) - window_size_correl + 1):
                window_series1 = series1[i:i + window_size_correl]
                window_series2 = series2[i:i + window_size_correl]
                cor = np.corrcoef(window_series1, window_series2)[0, 1]
                correl_values.append(cor)
            return np.array(correl_values)

        # Calculate and plot rolling correlation for each pair
        for i, (name1, name2) in enumerate(pairs):
            try:
                df1 = data[name1]
                df2 = data[name2]
            except KeyError as e:
                print(f"KeyError: {e} not found in data")
                continue

            # Compute the rolling correlation using derivatives
            corr_values = rolling_correlation(df1, df2, plt["window_size_correl"])

            # Plot the rolling correlation on a separate axis (y7)
            fig.add_trace(go.Scatter(
                x=dataframes_dvd[0].iloc[:len(corr_values), 0],
                y=corr_values,
                mode='lines',
                line=dict(color=color_palette[i % len(color_palette)], width=1),
                name=f'COR {name1}<br>{name2}'
            ), secondary_y=True)


        # Update plot layout for dual y-axes 
        plo["age_band"] = age_band
         
        # Function to update the x-axis title based on the type of plot
        def update_xaxis_title(is_standard_plot):
            if is_standard_plot:
                fig.update_xaxes(title='Day from 2020-01-01')
            else:
                fig.update_xaxes(title='Day from 2020-01-01', overlaying='x', side='bottom')

        # Update the layout of the figure
        fig.update_layout(
            colorway=color_palette,
            title=dict(
                text=f'{plo["title_text"]} AGE: {age_band}<br><br><sup>{plo["subtitle_text"]}</sup>',
                y=0.97,
                font=dict(size=18),
                x=0.2,  # Center the title
                xanchor='center',
                yanchor='top'
            ),
            yaxis=dict(title=plo["yaxis1_title"], side='left'),
            yaxis2=dict(title='Values y2 VD', anchor='free', position=0.05, side='left'),
            yaxis3=dict(title='Cumulative Values y3 VD', overlaying="y", position=0.9, side="right"),
            yaxis4=dict(title='Cumulative Values y4 VD', overlaying="y", side="right"),
            yaxis5=dict(title='1st and 2nd Derivative y5', overlaying="y", side="left", position=0.15),  # First derivative y5
            yaxis6=dict(title='1st and 2nd Derivative y6', overlaying="y", side="left", position=0.25),  # Second derivative y6
            yaxis7=dict(title='Rolling Pearson Correlation y7', overlaying='y', side='right', position=0.8),  # Pearson y7
            xaxis7=dict(title='Time', overlaying='x', side='bottom', position=0.5),  # Add this line for recurrence plot x-axis
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

        # Update trace assignment to the y-axes
        num_additional_traces = 55  # Adjust if this number changes

        # Go through all traces, excluding the additional ones
        for j in range(len(fig.data) - num_additional_traces):
            if j % 10 == 0 or j % 10 == 1:      # y1
                fig.data[j].update(yaxis='y1')
            elif j % 10 == 2 or j % 10 == 3:    # y5 for DVD derivatives and y6 for VD derivatives
                fig.data[j].update(yaxis='y5')  # First derivative of DVD or second derivative of DVD                           
            elif j % 10 == 4:  # y3
                fig.data[j].update(yaxis='y3')    
            elif j % 10 == 5 or j % 10 == 6:    # y2
                fig.data[j].update(yaxis='y2')
            elif j % 10 == 7 or j % 10 == 8:
                fig.data[j].update(yaxis='y6')  # First derivative of VD or second derivative of VD
            elif j % 10 == 9:  # y4
                fig.data[j].update(yaxis='y4')

        # Add pearson plot traces and update x-axis title accordingly
        is_standard_plot = True  # Set this flag to True when adding pearson plots

        for i in range(1, num_additional_traces + 1):
            fig.data[-i].update(yaxis='y7')

        # Update the x-axis title based on the presence of recurrence plots
        update_xaxis_title(is_standard_plot)

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
            f.write('        #legend { display: grid; grid-template-columns: repeat(10, 1fr); gap: 5px; margin-top: 20px; }\n') # Changed to 10 columns 
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
def init_plot_title(plt):        
    # generate plot name
    plot_name = f"AVGWD_{plt["window_size_mov_average"]} CORRWD_{plt["window_size_correl"]}"
    if plt["normalize"] == True : plot_name = f"NORM {plot_name}"
    if plt["normalize_cumulate_deaths"] : plot_name = f"N-CUM-D {plot_name}"        
    if plt["population_minus_death"] : plot_name = f"POP-D {plot_name}"
    plot_name = f"{plot_name}"
    print ( f"pltname: { plot_name }")    
    # plot title_text 
    title_text = plt["title_text"]        
    # generate pairs_text 
    #pairs_text = ""
    #for pair in pairs:
    #    pairs_text = f"{pairs_text} {pair[0].replace(" ", "").replace("Avg", "A")}-{pair[1].replace(" ", "").replace("Avg", "A")}"        
    #    pairs_text = pairs_text.lstrip()
    # generate subtitle text and axis text depending on choosed vars        
    subtitle_text = f"{''.join(textwrap.wrap(plot_name, 45, break_long_words=False, replace_whitespace=False))}<br>"    
    #subtitle_text = f"{subtitle_text}{pairs_text}<br>"    
    subtitle_text = f"{subtitle_text}<br>"        
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
        subtitle_text = f'{subtitle_text}Deaths were subtracted from population<br>'           
    else :
        subtitle_text = f'{subtitle_text}Deaths not! subtracted from population<br>'
    subtitle_text = f'{subtitle_text}To deselect all - double-click on a legend entry'
    return {"name": plot_name,
            #"pairs_text": pairs_text,
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
