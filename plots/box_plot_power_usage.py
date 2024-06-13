import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from extract_data import extract_performance_data, find_files_by_extension

if __name__ == "__main__":
    data_directory = "../data"

    performance_files = find_files_by_extension(data_directory, "_performance.xlsx")

    power_data_by_cpu = {}

    for file_path in performance_files:
        data = extract_performance_data(file_path)
        model_name = data['Main'].get('model', 'Unknown Model')
        cpu_type = data['Main'].get('cpu', 'Unknown CPU')
        power_df = data['Power Usages']

        if cpu_type not in power_data_by_cpu:
            power_data_by_cpu[cpu_type] = []

        power_df['Model'] = model_name

        power_data_by_cpu[cpu_type].append(power_df)

    unique_models = set()
    for cpu_type, df_list in power_data_by_cpu.items():
        for df in df_list:
            unique_models.update(df['Model'].unique())
    unique_models = sorted(unique_models)  # Sort models alphabetically

    colors = sns.color_palette('tab10', n_colors=len(unique_models))

    model_colors = {model: colors[i] for i, model in enumerate(unique_models)}

    for cpu_type, df_list in power_data_by_cpu.items():
        combined_df = pd.concat(df_list, ignore_index=True)

        combined_df['Model'] = pd.Categorical(combined_df['Model'], categories=unique_models, ordered=True)

        plt.figure(figsize=(12, 8))
        plt.title(f'Boxplot of Power Usage for CPU Type: {cpu_type}')
        plt.xlabel('Model')
        plt.ylabel('Power Usage (Watt)')
        plt.xticks(rotation=45)
        plt.grid(True)

        sns.boxplot(x='Model', y='power_watt', data=combined_df, hue='Model', palette=model_colors, dodge=False,
                    showfliers=False)

        plt.tight_layout()
        plt.show()
