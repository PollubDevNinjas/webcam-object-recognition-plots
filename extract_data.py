import os
import pandas as pd


def extract_accuracy_data(file_path):
    xls = pd.ExcelFile(file_path)

    main_df = pd.read_excel(xls, sheet_name="Main", index_col=0, header=None)

    main_data = main_df.squeeze().to_dict()

    detections_df = pd.read_excel(xls, sheet_name="Detections")

    extracted_data = {
        'Main': main_data,
        'Detections': detections_df
    }

    return extracted_data


def extract_performance_data(file_path):
    xls = pd.ExcelFile(file_path)

    main_df = pd.read_excel(xls, sheet_name="Main", index_col=0, header=None)

    main_data = main_df.squeeze().to_dict()

    resource_df = pd.read_excel(xls, sheet_name="Resource Usages")

    power_df = pd.read_excel(xls, sheet_name="Power Usages")

    extracted_data = {
        'Main': main_data,
        'Resource Usages': resource_df,
        'Power Usages': power_df
    }

    return extracted_data


def find_files_by_extension(directory, file_extension):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(file_extension):
                file_path = os.path.join(root, filename)
                matching_files.append(file_path)
    return matching_files
