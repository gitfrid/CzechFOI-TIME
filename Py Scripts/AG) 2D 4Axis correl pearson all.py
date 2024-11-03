import pandas as pd
import plotly.graph_objects as go
import os
import shutil
from plotly.subplots import make_subplots
import numpy as np
import textwrap
import plotly.express as px


def main():

    # set plot titele and the filename depending on choosed vars
    plt = {   
        "title_text": "Rolling pearson correlation",         
        "window_size_correl": 50,
        "window_size_mov_average": 14,
        "normalize": True,
        "normalize_cumulate_deaths": False,
        "population_minus_death": False,
        "correl_data_series" : ""
    } 

    pairs = [
            ('NUM_DUX','NUM_VDA'),
            ('NUM_DUVX','NUM_VDA' ),
            ('NUM_D','NUM_VDA' )
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
        
        # Define colors for rolling correlation curves 
        colors = ['orangered', 'yellowgreen', 'deepskyblue']  

        # Extract data from the traces
        data = {trace.name: trace.y for trace in fig.data}

        # Function to calculate rolling Correlation
        def rolling_correlation(series1, series2, window_size_correl):
            correl_values = []
            for i in range(len(series1) - window_size_correl + 1):
                window_series1 = series1[i:i + window_size_correl]
                window_series2 = series2[i:i + window_size_correl]
                cor = np.corrcoef(window_series1, window_series2)[0, 1]
                correl_values.append(cor)
            return np.array(correl_values)

        # Use the (moving average) data for the correlation calculation
        for i, (name1, name2) in enumerate(pairs):
            try:
                df1 = data[name1]
                df2 = data[name2]
            except KeyError as e:
                print(f"KeyError: {e} not found in moving_averages")
                continue
             
            # data for rolling correlation
            ccf_values = rolling_correlation(df1, df2, plt["window_size_correl"])
            
            # plot the rolling correlation at y5-axis
            fig.add_trace(go.Scatter(
                x=dataframes_dvd[0].iloc[:len(ccf_values), 0],
                y=ccf_values,
                mode='lines',
                line=dict(color=colors[i], width=1),
                name=f'COR {name1}<br>{name2}'
            ), secondary_y=True)        
        
        # Update plot layout for dual y-axes 
        plo["age_band"] = age_band       
        fig.update_layout(
            colorway=color_palette,
            title=dict( 
                text = f'{plo["title_text"]} AGE: {age_band}<br><br><sup>{plo["subtitle_text"]}</sup>',
                y=0.97, 
                font=dict(size=18),
                #x=0.5, 
                #xanchor='center', 
                yanchor='top'
            ),
            xaxis=dict(title='Day from 2020-01-01'),
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
                itemwidth=30,              
                orientation="h",
                yanchor="bottom",
                xanchor="right",
                y=1,
                x=0.9,  # adjust the x position to move the legend to the right                
                tracegroupgap=4, 
                font=dict(size=10)
            ),
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
        fig.write_html(f"{full_plotfile_name} AG_{age_band}.html")
        print(f"Plot {full_plotfile_name} {age_band} has been saved to HTML file.")



# Initialize the plot name - plot title text - axis text
def init_plot_title(plt,pairs):        
    # generate plot name
    plot_name = f"AVG_{plt["window_size_mov_average"]} CORR_{plt["window_size_correl"]}"
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
        subtitle_text = f'{subtitle_text}Deaths were subtracted from population<br>'           
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
