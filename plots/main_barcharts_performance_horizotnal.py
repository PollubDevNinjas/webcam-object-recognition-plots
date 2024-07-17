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


def plot_metrics(data, metric, std_metric, output_dir):
    plt.figure(figsize=(10, 8))  # Adjust figure size for horizontal plot
    unique_cpus = data['cpu'].unique()
    unique_models = data['model'].unique()
    bar_height = 0.2
    y_positions = range(len(unique_cpus))

    cpu_mapping = {}  # Dictionary to map PC numbers to CPU types

    for i, cpu in enumerate(unique_cpus):
        pc_label = f'PC{i + 1}'
        cpu_mapping[pc_label] = cpu

    for j, model in enumerate(unique_models):
        model_data = data[data['model'] == model]
        offsets = [i + j * bar_height for i in y_positions]
        x_values = model_data[metric].values
        if std_metric:
            x_errors = model_data[std_metric].values
        else:
            x_errors = None

        plt.barh(offsets, x_values, height=bar_height, label=model, xerr=x_errors, capsize=5)

    plt.yticks([r + bar_height * (len(unique_models) - 1) / 2 for r in y_positions], list(cpu_mapping.keys()),
               fontsize=16)
    plt.title(f'Comparison of {metric} across models and CPUs', fontsize=20)
    plt.xlabel(metric, fontsize=20)
    plt.ylabel('PC Number', fontsize=20)

    # Adding vertical lines for x-axis labels
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.legend(title='Model', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{metric}_comparison.png'))
    plt.close()

    # Print correspondence between PC labels and CPU types
    print("PC Label Correspondence:")
    for pc_label, cpu_type in cpu_mapping.items():
        print(f"{pc_label}: {cpu_type}")


def main(data_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    performance_data = load_performance_data(data_directory)

    metrics = {
        'avg_detection_time': None,
        'avg_cpu_usage': 'cpu_usage_std',
        'cpu_freq_avg': 'cpu_freq_std',
        'avg_cpu_package_power': 'cpu_package_power_std',
        'avg_cpu_package_temp': 'cpu_package_temp_std',
        'avg_memory_usage': 'memory_usage_std',
        'avg_power_usage': 'power_usage_std'
    }

    for metric, std_metric in metrics.items():
        plot_metrics(performance_data, metric, std_metric, output_directory)


if __name__ == '__main__':
    data_directory = '../data'
    output_directory = '../output'
    main(data_directory, output_directory)
