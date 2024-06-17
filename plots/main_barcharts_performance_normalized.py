import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from extract_data import extract_performance_data, find_files_by_extension

def load_performance_data(directory):
    files = find_files_by_extension(directory, '_performance.xlsx')
    data = []
    for file in files:
        extracted_data = extract_performance_data(file)
        main_data = extracted_data['Main']

        # Extracting specific data and adding it to a dictionary
        performance_data = {
            'date': main_data.get('date'),
            'cpu': main_data.get('cpu'),
            'model': main_data.get('model'),
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
            'file': os.path.basename(file)  # Add file name for reference
        }

        data.append(performance_data)

    return pd.DataFrame(data)

def normalize_data(df, metric):
    df[f'{metric}_normalized'] = (df[metric] - df[metric].min()) / (df[metric].max() - df[metric].min())
    return df

def plot_normalized_metrics(data, metric, output_dir):
    plt.figure(figsize=(10, 8))  # Adjust figure size for horizontal plot
    unique_models = data['model'].unique()
    bar_height = 0.4
    y_positions = range(len(unique_models))

    for i, model in enumerate(unique_models):
        model_data = data[data['model'] == model]
        normalized_metric = f'{metric}_normalized'
        plt.barh(y_positions[i], model_data[normalized_metric].mean(), height=bar_height, label=model)

    plt.yticks(y_positions, unique_models)
    plt.title(f'Normalized Comparison of {metric} across Models')
    plt.xlabel(f'Normalized {metric}')
    plt.ylabel('Model')
    plt.legend(title='Model')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{metric}_normalized_comparison.png'))
    plt.close()

def main(data_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    performance_data = load_performance_data(data_directory)

    metrics = [
        'avg_detection_time',
        'avg_cpu_usage',
        'cpu_freq_avg',
        'avg_cpu_package_power',
        'avg_cpu_package_temp',
        'avg_memory_usage',
        'avg_power_usage'
    ]

    for metric in metrics:
        performance_data = normalize_data(performance_data, metric)
        plot_normalized_metrics(performance_data, metric, output_directory)

if __name__ == '__main__':
    data_directory = '../data'
    output_directory = '../output_normalized_horizontal'
    main(data_directory, output_directory)
