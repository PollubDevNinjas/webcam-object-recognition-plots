import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from extract_data import extract_performance_data, find_files_by_extension


def plot_metric_over_time(data_by_cpu, metric, ylabel, title, model_colors):
    unique_models = sorted(
        set(model for df_list in data_by_cpu.values() for df in df_list for model in df['Model'].unique()))

    for cpu_type, df_list in data_by_cpu.items():
        plt.figure(figsize=(12, 8))
        plt.title(f'{title} for CPU Type: {cpu_type}')
        plt.xlabel('Elapsed Time (%)')
        plt.ylabel(ylabel)

        for model in unique_models:
            for df in df_list:
                if model in df['Model'].unique():
                    sns.lineplot(x='elapsed_time_percent', y=metric, data=df[df['Model'] == model], label=model,
                                 color=model_colors[model])

        plt.legend(title='Model', loc='lower right', bbox_to_anchor=(1, 0))
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def process_and_interpolate_data(df):
    """
    Process the DataFrame to ensure it has exactly 240 points.
    If the DataFrame has fewer than 240 points, interpolate the data.
    If the DataFrame has more than 240 points, downsample the data.
    """
    target_points = 240
    df = df.sort_values(by='elapsed_time_percent')

    if len(df) < target_points:
        # Interpolate to get 240 points
        interp_df = pd.DataFrame({
            'elapsed_time_percent': np.linspace(0, 100, target_points)
        })
        for column in df.columns:
            if column != 'elapsed_time_percent' and column != 'Model':
                interp_df[column] = np.interp(interp_df['elapsed_time_percent'], df['elapsed_time_percent'], df[column])
        interp_df['Model'] = df['Model'].iloc[0]  # Keep the model name consistent
    elif len(df) > target_points:
        # Downsample to get 240 points
        indices = np.linspace(0, len(df) - 1, target_points).astype(int)
        interp_df = df.iloc[indices].reset_index(drop=True)
    else:
        # Already has 240 points
        interp_df = df

    return interp_df


if __name__ == "__main__":
    data_directory = "../data"

    performance_files = find_files_by_extension(data_directory, "_performance.xlsx")

    resource_data_by_cpu = {}

    for file_path in performance_files:
        data = extract_performance_data(file_path)
        model_name = data['Main'].get('model', 'Unknown Model')
        cpu_type = data['Main'].get('cpu', 'Unknown CPU')
        resource_df = data['Resource Usages']
        resource_df['Model'] = model_name

        # Convert elapsed time to percentage of completion
        max_elapsed_time = resource_df['elapsed_time'].max()
        resource_df['elapsed_time_percent'] = (resource_df['elapsed_time'] / max_elapsed_time) * 100

        # Process and interpolate data
        resource_df = process_and_interpolate_data(resource_df)

        if cpu_type not in resource_data_by_cpu:
            resource_data_by_cpu[cpu_type] = []

        resource_data_by_cpu[cpu_type].append(resource_df)

    unique_models = set()
    for cpu_type, df_list in resource_data_by_cpu.items():
        for df in df_list:
            unique_models.update(df['Model'].unique())
    unique_models = sorted(unique_models)

    colors = sns.color_palette('tab10', n_colors=len(unique_models))
    model_colors = {model: colors[i] for i, model in enumerate(unique_models)}

    # Plot memory usage over time
    plot_metric_over_time(resource_data_by_cpu, 'memory_mb', 'Memory Usage (MB)', 'Memory Usage Over Time',
                          model_colors)

    # Plot CPU usage over time
    plot_metric_over_time(resource_data_by_cpu, 'cpu_usage', 'CPU Usage (%)', 'CPU Usage Over Time', model_colors)

    # Plot package power usage over time
    plot_metric_over_time(resource_data_by_cpu, 'cpu_package_power', 'Package Power Usage (Watt)',
                          'Package Power Usage Over Time', model_colors)

    # Plot CPU package temperature over time
    plot_metric_over_time(resource_data_by_cpu, 'cpu_package_temp', 'CPU Package Temperature (°C)',
                          'CPU Package Temperature Over Time', model_colors)
