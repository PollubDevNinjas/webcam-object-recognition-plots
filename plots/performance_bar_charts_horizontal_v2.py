import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

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


# Load the performance data
data = load_performance_data('../data')


# Draw horizontal bar charts
def draw_bar_charts(df):
    stats = [
        'avg_detection_time', 'avg_cpu_usage', 'cpu_freq_avg',
        'avg_cpu_package_power', 'avg_cpu_package_temp',
        'avg_memory_usage', 'avg_power_usage', 'fps'
    ]

    for stat in stats:
        plt.figure(figsize=(12, 8))
        sns.barplot(
            data=df,
            y='model_short_name',
            x=stat,
            hue='cpu_short_name',
            orient='h'
        )
        plt.title(f'{stat.replace("_", " ").title()} by Model and CPU')
        plt.xlabel(stat.replace("_", " ").title())
        plt.ylabel('Model Name')
        plt.legend( bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol = 4)
        plt.tight_layout()
        plt.show()


# Ensure the data is correct
print(data)

# Draw the bar charts
draw_bar_charts(data)