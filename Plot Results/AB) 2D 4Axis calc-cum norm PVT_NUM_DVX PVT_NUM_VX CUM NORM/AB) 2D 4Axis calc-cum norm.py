import pandas as pd
import plotly.graph_objects as go
import os
import shutil
from plotly.subplots import make_subplots


def main():
    
    plot_name = "PVT_NUM_DVX PVT_NUM_VX CUM NORM"

    # List of CSV file paths
    csv_files = [
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_DVX.csv",
        r"C:\CzechFOI-TIME\TERRA\PVT_NUM_VX.csv",
    ]

    # Generate output file paths by appending "CUM" after "PVT_"
    csv_files_cum = [
        os.path.join(os.path.dirname(file), os.path.basename(file).replace("PVT_", "PVT_CUM_"))
        for file in csv_files
    ]

    # Read all CSV files into a list of DataFrames
    dataframes = [pd.read_csv(file) for file in csv_files]

    # Get the list of age bands from the columns (excluding the first column which is 'DAY')
    age_bands = dataframes[0].columns[1:]

    # Calculate cumulative values for the DataFrames
    cumulative_dataframes = []
    for df in dataframes:
        df_cumulative = df.copy()
        df_cumulative[age_bands] = df[age_bands].cumsum()
        cumulative_dataframes.append(df_cumulative)

    # Save the cumulative DataFrames to the generated CSV files
    for cum_df, output_file in zip(cumulative_dataframes, csv_files_cum):
        cum_df.to_csv(output_file, index=False)
    print("Cumulative data saved to CSV files successfully.")

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)
    
    # ** Normalize the data per 100,000 for the first CSV file **
    # ** Used to check if compared with the normalized pivot data by SQLite query gives same plot result **
    for age_band in age_bands:
        dataframes[0][age_band] = (dataframes[0][age_band] / cumulative_dataframes[1][age_band]) * 100000
    # Debug - save the normalized DataFrame to a CSV file
    # dataframes[0].to_csv(f'{full_plotfile_name} normalized.csv', index=False)

    # Create a plot for each age band
    for age_band in age_bands:
        fig = go.Figure()
        
        # Create subplots with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Filter dataframes to include only values where x >= 800
        filtered_df0 = dataframes[0][dataframes[0].iloc[:, 0] >= 800]
        filtered_df1 = dataframes[1][dataframes[1].iloc[:, 0] >= 800]
        filtered_cum_df0 = cumulative_dataframes[0][cumulative_dataframes[0].iloc[:, 0] >= 800]
        filtered_cum_df1 = cumulative_dataframes[1][cumulative_dataframes[1].iloc[:, 0] >= 800]
        
        # Add traces for the first two CSV files on the primary y-axis
        fig.add_trace(go.Scatter(x=filtered_df0.iloc[:, 0], y=filtered_df0[age_band], mode='lines', name=csv_files[0]), secondary_y=False)
        fig.add_trace(go.Scatter(x=filtered_df1.iloc[:, 0], y=filtered_df1[age_band], mode='lines', name=csv_files[1]), secondary_y=False)

        # Add traces for the cumulative data on the secondary y-axis
        fig.add_trace(go.Scatter(x=filtered_cum_df0.iloc[:, 0], y=filtered_cum_df0[age_band], mode='lines', name=csv_files_cum[0]), secondary_y=True)
        fig.add_trace(go.Scatter(x=filtered_cum_df1.iloc[:, 0], y=filtered_cum_df1[age_band], mode='lines', name=csv_files_cum[1]), secondary_y=True)

        # Update layout for dual y-axes
        fig.update_layout(
            title=f'Age Group {plot_name} : {age_band}',
            xaxis=dict(title='Day from 2020-01-01'),
            yaxis=dict(
                title=f'Values per 100,000 {os.path.splitext(os.path.basename(csv_files[0]))[0]}',
                side='left'                
            ),
            yaxis2=dict(
                title=f'Values {os.path.splitext(os.path.basename(csv_files[1]))[0]}',
                anchor='free',
                position=0.05,
                side='left'                
            ),
            yaxis3=dict(
                title=f"Cumulative Values {os.path.splitext(os.path.basename(csv_files_cum[0]))[0]}",
                overlaying="y",
                side="right",
                position=0.9
            ),
            yaxis4=dict(
                title=f"Cumulative Values {os.path.splitext(os.path.basename(csv_files_cum[1]))[0]}",
                overlaying="y",
                side="right",                
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=0.8                
            )            
        )
        
        # Update traces to use the new y-axes
        fig.data[0].update(yaxis='y1')
        fig.data[1].update(yaxis='y2')
        fig.data[2].update(yaxis='y3')
        fig.data[3].update(yaxis='y4')

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
