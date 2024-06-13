import os
import matplotlib.pyplot as plt
import seaborn as sns
from extract_data import extract_performance_data, find_files_by_extension


def plot_metric_over_time(data_by_cpu, metric, ylabel, title, model_colors):
    unique_models = sorted(
        set(model for df_list in data_by_cpu.values() for df in df_list for model in df['Model'].unique()))

    for cpu_type, df_list in data_by_cpu.items():
        plt.figure(figsize=(12, 8))
        plt.title(f'{title} for CPU Type: {cpu_type}')
        plt.xlabel('Elapsed Time (seconds)')
        plt.ylabel(ylabel)

        for model in unique_models:
            for df in df_list:
                if model in df['Model'].unique():
                    sns.lineplot(x='elapsed_time', y=metric, data=df[df['Model'] == model], label=model,
                                 color=model_colors[model])

        plt.legend(title='Model', loc='upper left', bbox_to_anchor=(1, 1))
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    data_directory = "../data"

    performance_files = find_files_by_extension(data_directory, "_performance.xlsx")

    resource_data_by_cpu = {}

    for file_path in performance_files:
        data = extract_performance_data(file_path)
        model_name = data['Main'].get('model', 'Unknown Model')
        cpu_type = data['Main'].get('cpu', 'Unknown CPU')
        resource_df = data['Resource Usages']

        if cpu_type not in resource_data_by_cpu:
            resource_data_by_cpu[cpu_type] = []

        resource_df['Model'] = model_name

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
