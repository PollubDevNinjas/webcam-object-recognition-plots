import matplotlib.pyplot as plt
from extract_data import extract_accuracy_data, find_files_by_extension

if __name__ == "__main__":
    data_directory = "../data"

    accuracy_files = find_files_by_extension(data_directory, "_accuracy.xlsx")

    merged_data = {}

    for file_path in accuracy_files:
        data = extract_accuracy_data(file_path)
        model_name = data['Main'].get('model', 'Unknown Model')
        detections_df = data['Detections']

        correct_count = (detections_df['is_correct'] == 1).sum()
        incorrect_count = (detections_df['is_correct'] == 0).sum()

        if model_name in merged_data:
            merged_data[model_name]['Correct'] += correct_count
            merged_data[model_name]['Incorrect'] += incorrect_count
        else:
            merged_data[model_name] = {'Correct': correct_count, 'Incorrect': incorrect_count}

    models = list(merged_data.keys())
    correct_counts = [merged_data[model]['Correct'] for model in models]
    incorrect_counts = [merged_data[model]['Incorrect'] for model in models]

    total_counts = [correct + incorrect for correct, incorrect in zip(correct_counts, incorrect_counts)]
    correct_percentages = [100 * correct / total if total > 0 else 0 for correct, total in
                           zip(correct_counts, total_counts)]
    incorrect_percentages = [100 * incorrect / total if total > 0 else 0 for incorrect, total in
                             zip(incorrect_counts, total_counts)]

    plt.figure(figsize=(12, 8))

    bar_width = 0.35
    index = range(len(models))

    bars1 = plt.bar(index, correct_percentages, bar_width, label='Correct', color='green')
    bars2 = plt.bar(index, incorrect_percentages, bar_width, label='Incorrect', color='red', bottom=correct_percentages)

    plt.xlabel('Model')
    plt.ylabel('Percentage of Detections (%)')
    plt.title('Correct vs Incorrect Detections by Model')
    plt.xticks(index, models, rotation=45)
    plt.legend()

    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        total_height = height1 + height2
        plt.text(bar1.get_x() + bar1.get_width() / 2., height1 / 2., f'{height1:.1f}%', ha='center', va='center',
                 color='white', fontsize=10)
        plt.text(bar2.get_x() + bar2.get_width() / 2., height1 + height2 / 2., f'{height2:.1f}%', ha='center',
                 va='center', color='white', fontsize=10)

    plt.tight_layout()
    plt.show()
