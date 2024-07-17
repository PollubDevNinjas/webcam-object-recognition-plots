import os
import pandas as pd
import numpy as np
from extract_data import extract_accuracy_data, find_files_by_extension

# Directory to traverse
data_dir = 'data'

# Find all files ending with _accuracy.xlsx
accuracy_files = find_files_by_extension(data_dir, '_accuracy.xlsx')

# Dictionary to hold combined detections for each model type
detections_data = {}

# Process each accuracy file
for file_path in accuracy_files:
    data = extract_accuracy_data(file_path)

    # Extract model type from the 'Main' data
    main_data = data['Main']
    model_type = main_data['model']

    # Extract detections dataframe
    detections_df = data['Detections']

    # Add detections dataframe to the dictionary
    if model_type not in detections_data:
        detections_data[model_type] = detections_df
    else:
        detections_data[model_type] = pd.concat([detections_data[model_type], detections_df])

# Calculate metrics for each model type
for model_type, detections_df in detections_data.items():
    average_detection_time = detections_df['time'].mean()
    detection_time_std = detections_df['time'].std()
    average_accuracy = detections_df['is_correct'].mean()

    # Filter out rows where is_correct is False (0) before calculating score metrics
    correct_detections_df = detections_df[detections_df['is_correct'] == True]
    average_score = correct_detections_df['score'].mean()
    score_std = correct_detections_df['score'].std()

    # Calculate FPS as 1 / average detection time
    fps = 1 / average_detection_time

    print(f'Model: {model_type}')
    print(f'Average Detection Time: {average_detection_time}')
    print(f'Detection Time Std Dev: {detection_time_std}')
    print(f'Average Accuracy: {average_accuracy}')
    print(f'Average Score: {average_score}')
    print(f'Score Std Dev: {score_std}')
    print(f'FPS: {fps}')
    print('-----------------------------------')
