import pandas as pd
import plotly.graph_objects as go
import os
import shutil
from plotly.subplots import make_subplots


def main():
    
    plot_name = "PVT_NUM_D PVT_NUM_VD CUM"

    # List of DVD CSV file paths
    csv_files_dvd = [
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_D.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DUVX.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVX.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVD1.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVD2.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVD3.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVD4.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVD5.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVD6.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVD7.csv",
    ]

    # List of VD CSV file paths
    csv_files_vd = [        
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_POP.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_UVX.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VX.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VD1.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VD2.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VD3.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VD4.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VD5.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VD6.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VD7.csv",        
    ]

    # Generate output file paths by appending "CUM" after "PVT_"
    csv_files_cum_dvd = [
        os.path.join(os.path.dirname(file), os.path.basename(file).replace("PVT_", "PVT_CUM_"))
        for file in csv_files_dvd
    ]

    # Generate output file paths by appending "CUM" after "PVT_"
    csv_files_cum_vd = [
        os.path.join(os.path.dirname(file), os.path.basename(file).replace("PVT_", "PVT_CUM_"))
        for file in csv_files_vd
    ]

    # Read all CSV files into a list of DataFrames
    dataframes_dvd = [pd.read_csv(file) for file in csv_files_dvd]
    dataframes_vd = [pd.read_csv(file) for file in csv_files_vd]

    # Get the list of age bands from the columns (excluding the first column which is 'DAY')
    age_bands = dataframes_dvd[0].columns[1:]

    # Calculate cumulative values for the dvd DataFrames
    cumulative_dataframes_dvd = []
    for df in dataframes_dvd:
        df_cumulative_dvd = df.copy()
        df_cumulative_dvd[age_bands] = df[age_bands].cumsum()
        cumulative_dataframes_dvd.append(df_cumulative_dvd)

    # Calculate cumulative values for the vd DataFrames
    # Deaths are excluded from the population, have been subtracted.
    cumulative_dataframes_vd = []
    for i, df in enumerate(dataframes_vd):
        df_cumulative_vd = df.copy()         
        if i == 0:
            print("This is the first dataframe.")
            df_cumulative_vd[age_bands] = dataframes_vd[0][age_bands] - dataframes_dvd[0][age_bands].cumsum()
        elif i == 1:
             print("This is the second dataframe.")
             df_cumulative_vd[age_bands] = dataframes_vd[0][age_bands] + df[age_bands].cumsum() - cumulative_dataframes_dvd[1][age_bands]
        elif i == 2:
             print("This is the third dataframe.")
             df_cumulative_vd[age_bands] = df[age_bands].cumsum() - cumulative_dataframes_dvd[2][age_bands]
        else:
             df_cumulative_vd = df.copy()
             df_cumulative_vd[age_bands] = df[age_bands].cumsum()
        cumulative_dataframes_vd.append(df_cumulative_vd)

    # Save the cumulative DataFrames to the generated CSV files
    for cum_df, output_file in zip(cumulative_dataframes_dvd, csv_files_cum_dvd):
        cum_df.to_csv(output_file, index=False)
    for cum_df, output_file in zip(cumulative_dataframes_vd, csv_files_cum_vd):
        cum_df.to_csv(output_file, index=False)
    print("Cumulative data saved to CSV files successfully.")

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)
    
    # Normalize the data per 100,000
    #for i in range(0, len(dataframes_dvd)):
    #    for age_band in age_bands:    
    #        dataframes_dvd[i][age_band] = (dataframes_dvd[i][age_band] / cumulative_dataframes_vd[i][age_band]) * 100000
            # Debug - save the normalized DataFrame to a CSV file
            #dataframes_dvd[i].to_csv(f'{full_plotfile_name} dvd normalized.csv', index=False)

    # Create a plot for each age band        
    for age_band in age_bands:  
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        
        for i in range(0,len(dataframes_dvd)):        
            print(f"i is {i}")
   
            # Add traces for each CSV file on the primary y-axis
            fig.add_trace(go.Scatter(x=dataframes_dvd[i].iloc[:, 0], y=dataframes_dvd[i][age_band], mode='lines',line=dict(dash='solid'), name=os.path.splitext(os.path.basename(csv_files_dvd[i]))[0]), secondary_y=False)
            fig.add_trace(go.Scatter(x=dataframes_vd[i].iloc[:, 0], y=dataframes_vd[i][age_band], mode='lines',line=dict(dash='dot'), name=os.path.splitext(os.path.basename(csv_files_vd[i]))[0]), secondary_y=False)
            # Add traces for the cumulative data on the secondary y-axis
            fig.add_trace(go.Scatter(x=cumulative_dataframes_dvd[i].iloc[:, 0], y=cumulative_dataframes_dvd[i][age_band], mode='lines',line=dict(dash='solid'), name=f'cumulative {os.path.splitext(os.path.basename(csv_files_dvd[i]))[0]}'), secondary_y=True)
            fig.add_trace(go.Scatter(x=cumulative_dataframes_vd[i].iloc[:, 0], y=cumulative_dataframes_vd[i][age_band], mode='lines', line=dict(dash='dot'), name=f'cumulative {os.path.splitext(os.path.basename(csv_files_vd[i]))[0]}'), secondary_y=True)

        # Update layout for dual y-axes
        fig.update_layout(
            title=(f'Age Group {plot_name} : {age_band} <br>'
                   '<sup>Deaths are excluded from the population, have been subtracted.<br>' 
                   'Deselect all - double-click on a legend entry</sup>'), 
            xaxis=dict(title='Day from 2020-01-01'),
            yaxis=dict(
                title=f'Values y1 DVD',
                side='left'                
            ),
            yaxis2=dict(
                title=f'Values y2 VD',
                anchor='free',
                position=0.05,
                side='left'                
            ),
            yaxis3=dict(
                title=f"Cumulative Values y3 DVD",
                overlaying="y",
                side="right",
                position=0.9
            ),
            yaxis4=dict(
                title=f"Cumulative Values y4 VD",
                overlaying="y",
                side="right",                
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=0.9                
            )            
        )
        
        # Update traces to use the new y-axes
        for j in range(len(fig.data)):
            if j % 4 == 0:
                fig.data[j].update(yaxis='y1')
            elif j % 4 == 1:
                fig.data[j].update(yaxis='y2')
            elif j % 4 == 2:
                fig.data[j].update(yaxis='y3')
            elif j % 4 == 3:
                fig.data[j].update(yaxis='y4')
        
        # Save the plot to an HTML file
        fig.write_html(f"{full_plotfile_name} {age_band}.html")
        print(f"Plot {full_plotfile_name} {age_band} has been saved to HTML file.")

# Initialize the "Plot Results" directory and copy this PyScript into it
def init_function(plot_name):
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    first_root_dir = os.path.abspath(os.sep.join(script_dir.split(os.sep)[:2]))
    plot_result_path = os.path.join(first_root_dir, "Plot Results", f"{script_name} {plot_name}")
    os.makedirs(plot_result_path, exist_ok=True)
    
    script_file_name = os.path.join(plot_result_path, f"{script_name}.py")
    if not os.path.exists(script_file_name):
        shutil.copy(__file__, script_file_name)
    # return plot file name without extension
    return plot_result_path + os.sep + f"{script_name} {plot_name}"

# call main script
if __name__ == "__main__": main()
