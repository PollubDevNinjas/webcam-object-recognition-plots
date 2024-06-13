import matplotlib.pyplot as plt
from extract_data import extract_performance_data, find_files_by_extension

if __name__ == "__main__":
    data_directory = "data"

    performance_files = find_files_by_extension(data_directory, "_performance.xlsx")

    power_usage_data = {}

    for file_path in performance_files:
        data = extract_performance_data(file_path)
        model_name = data['Main'].get('model', 'Unknown Model')
        cpu_type = data['Main'].get('cpu', 'Unknown CPU')
        power_df = data['Power Usages']

        if cpu_type not in power_usage_data:
            power_usage_data[cpu_type] = []

        power_usage_data[cpu_type].append((model_name, power_df))

    for cpu_type, model_data_list in power_usage_data.items():
        plt.figure(figsize=(10, 6))
        plt.title(f'Power Usage Over Time for {cpu_type}')
        plt.xlabel('Elapsed Time')
        plt.ylabel('Power Usage (Watt)')

        for model_name, df in model_data_list:
            plt.plot(df['elapsed_time'], df['power_watt'], label=model_name)

        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
