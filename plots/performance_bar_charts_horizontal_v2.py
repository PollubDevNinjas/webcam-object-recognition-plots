import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

from extract_data import extract_performance_data, find_files_by_extension


def load_performance_data(directory):
    files = find_files_by_extension(directory, '_performance.xlsx')
    data = []
    cpus = {
        'Intel(R) Core(TM) i5-4200H CPU @ 2.80GHz': 'PC1',
        'Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz': 'PC2',
        'AMD Ryzen 5 5600 6-Core Processor': 'PC3',
        'AMD Ryzen 5 2600 Six-Core Processor': 'PC4'
    }
    models = {
        'yolov8s': 'yolo v8 s',
        'ssd_mobilenet_v2_fpnlite_320x320': 'mobile net v2',
        'efficient_det_lite1': 'efficient det lite 1',
        'efficient_det_lite2': 'efficient det lite 2',
        'efficient_det_lite3': 'efficient det lite 3',
        'faster_rcnn_resnet101_v1_640x640': 'faster rcnn'
    }
    for file in files:
        extracted_data = extract_performance_data(file)
        main_data = extracted_data['Main']

        # Extracting specific data and adding it to a dictionary
        performance_data = {
            'date': main_data.get('date'),
            'cpu': main_data.get('cpu'),
            'cpu_short_name': cpus.get(main_data.get('cpu')),
            'model': main_data.get('model'),
            'model_short_name': models.get(main_data.get('model')),
            'avg_detection_time': main_data.get('average_detection_time'),
            'avg_cpu_usage': main_data.get('avg_cpu_usage'),
            'cpu_usage_std': main_data.get('cpu_usage_std'),
            'cpu_freq_avg': main_data.get('cpu_freq_avg'),
            'cpu_freq_std': main_data.get('cpu_freq_std'),
            'avg_cpu_package_power': main_data.get('avg_cpu_package_power'),
            'cpu_package_power_std': main_data.get('cpu_package_power_std'),
            'avg_cpu_package_temp': main_data.get('avg_cpu_package_temp'),
            'cpu_package_temp_std': main_data.get('cpu_package_temp_std'),
            'avg_memory_usage': main_data.get('avg_memory_usage'),
            'memory_usage_std': main_data.get('memory_usage_std'),
            'avg_power_usage': main_data.get('avg_power_usage'),
            'power_usage_std': main_data.get('power_usage_std'),
            'fps': main_data.get('fps'),
            'file': os.path.basename(file)
        }

        data.append(performance_data)

    return pd.DataFrame(data)


def draw_bar_charts(df, titles=None, x_labels=None, output_dir='horizontal_bar_plots_v2'):
    stats = {
        'avg_cpu_usage': 'cpu_usage_std',
        'cpu_freq_avg': 'cpu_freq_std',
        'avg_cpu_package_power': 'cpu_package_power_std',
        'avg_cpu_package_temp': 'cpu_package_temp_std',
        'avg_memory_usage': 'memory_usage_std',
        'avg_power_usage': 'power_usage_std',
        'fps': None
    }

    # Set default titles if none are provided
    if titles is None:
        titles = {
            'avg_cpu_usage': 'Average CPU Usage with Standard Deviation',
            'cpu_freq_avg': 'Average CPU Frequency with Standard Deviation',
            'avg_cpu_package_power': 'Average CPU Package Power with Standard Deviation',
            'avg_cpu_package_temp': 'Average CPU Package Temperature with Standard Deviation',
            'avg_memory_usage': 'Average Memory Usage with Standard Deviation',
            'avg_power_usage': 'Average Power Usage with Standard Deviation',
            'fps': 'Frames Per Second'
        }

    # Set default x-axis labels if none are provided
    if x_labels is None:
        x_labels = {
            'avg_cpu_usage': 'Average CPU Usage (%)',
            'cpu_freq_avg': 'Average CPU Frequency (GHz)',
            'avg_cpu_package_power': 'Average CPU Package Power (W)',
            'avg_cpu_package_temp': 'Average CPU Package Temperature (°C)',
            'avg_memory_usage': 'Average Memory Usage (GB)',
            'avg_power_usage': 'Average Power Usage (W)',
            'fps': 'Frames Per Second'
        }

    for stat, std in stats.items():
        plt.figure(figsize=(12, 8))

        if std:  # If there is a standard deviation column for the stat
            # Compute the mean values
            grouped = df.groupby(['model_short_name', 'cpu_short_name'])
            mean_values = grouped[stat].mean().reset_index()

            # Compute the average standard deviation using the formula
            std_squared = grouped[std].apply(lambda x: np.mean(x ** 2)).reset_index(name='std_squared')
            avg_std = np.sqrt(std_squared['std_squared'])

            # Add the average standard deviation to the mean values
            mean_values[std] = avg_std

            # Plot the bars with error bars
            ax = sns.barplot(
                data=mean_values,
                y='model_short_name',
                x=stat,
                hue='cpu_short_name',
                orient='h',
                errorbar=None  # Disable default confidence intervals
            )

            # Add error bars
            for i, (patch, err) in enumerate(zip(ax.patches, mean_values[std])):
                # Get the x position and height of the bar
                x = patch.get_width()
                y = patch.get_y() + patch.get_height() / 2
                plt.errorbar(
                    x=x,
                    y=y,
                    xerr=err,
                    color='black',
                    capsize=5,
                    elinewidth=1,
                    zorder=5  # Ensure error bars are drawn on top of bars
                )
        else:
            # Compute only the mean values if no std exists
            mean_values = df.groupby(['model_short_name', 'cpu_short_name'])[stat].mean().reset_index()
            mean_values[std] = np.nan  # Placeholder for std to avoid errors

            ax = sns.barplot(
                data=mean_values,
                y='model_short_name',
                x=stat,
                hue='cpu_short_name',
                orient='h',
                ci=None  # Disable default confidence intervals
            )

        # Use the provided title if it exists, otherwise use a default title
        plot_title = titles.get(stat, f'{stat.replace("_", " ").title()} dla modelu i maszyny')
        plt.title(plot_title)

        # Use the provided x-axis label if it exists, otherwise use a default label
        x_axis_label = x_labels.get(stat, stat.replace("_", " ").title())
        plt.xlabel(x_axis_label)
        plt.ylabel('Model')

        # Add grid lines for better readability
        plt.grid(axis='x', linestyle='--', linewidth=0.7, color='gray')
        ax.yaxis.grid(True, linestyle='--', linewidth=0.7, color='gray')

        plt.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=4)

        plt.tight_layout()
        plt.show()

custom_titles = {
    'avg_cpu_usage': 'Średnie zużycie procesora',
    'cpu_freq_avg': 'Średnie taktowanie procesora',
    'avg_cpu_package_power': 'Śreni pobór mocy procesora',
    'avg_cpu_package_temp': 'Śrenia temperatura procesora',
    'avg_memory_usage': 'Średnie zużycie pamięci',
    'avg_power_usage': 'Średni pobór mocy',
    'fps': 'Średnia ilość FPS'
}

custom_x_labels = {
    'avg_cpu_usage': 'Średnie zużycie procesora (%)',
    'cpu_freq_avg': 'Średnie taktowanie procesora (MHz)',
    'avg_cpu_package_power': 'Śreni pobór mocy procesora (W)',
    'avg_cpu_package_temp': 'Śrenia temperatura procesora (°C)',
    'avg_memory_usage': 'Średnie zużycie pamięci (MB)',
    'avg_power_usage': 'Średni pobór mocy (W)',
    'fps': 'Średnia ilość FPS'
}

# Load the performance data
data = load_performance_data('../data')

# Draw the bar charts with custom titles and x-axis labels
draw_bar_charts(data, titles=custom_titles, x_labels=custom_x_labels)