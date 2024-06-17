import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from extract_data import extract_accuracy_data, find_files_by_extension

if __name__ == "__main__":
    data_directory = "../data"

    accuracy_files = find_files_by_extension(data_directory, "_accuracy.xlsx")

    all_detections = []

    for file_path in accuracy_files:
        data = extract_accuracy_data(file_path)
        model_name = data['Main'].get('model', 'Unknown Model')
        detections_df = data['Detections']

        detections_df['Model'] = model_name

        all_detections.append(detections_df)

    combined_df = pd.concat(all_detections, ignore_index=True)

    unique_models = combined_df['Model'].unique()
    colors = sns.color_palette('tab10', n_colors=len(unique_models))

    model_colors = {model: colors[i] for i, model in enumerate(unique_models)}

    plt.figure(figsize=(12, 8))
    plt.title('Boxplot of Scores for Different Models', fontsize = 20)
    plt.xlabel('Model', fontsize = 20)
    plt.ylabel('Score', fontsize = 20)
    plt.xticks(rotation=45, fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)

    sns.boxplot(x='Model', y='score', data=combined_df, hue='Model', palette=model_colors, dodge=False,
                showfliers=False)

    plt.legend().set_visible(False)  # Hide legend to comply with the warning
    plt.tight_layout()
    plt.show()
