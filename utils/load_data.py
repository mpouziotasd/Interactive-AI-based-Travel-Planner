import pandas as pd

def load_data(csv_file, dtypes):
    # Load the data with enforced dtypes
    df_data = pd.read_csv(
            csv_file,
            dtype=dtypes,
            sep=',',
            on_bad_lines='skip',
            quotechar='"',
            escapechar='\\'
        )
    return df_data

