import os
import pandas as pd


def files_concater(directory: str, prefix: str) -> pd.DataFrame:
    # Get a list of all Excel files in the directory with the specified prefix
    files = [
        f
        for f in os.listdir(directory)
        if f.startswith(prefix) and (f.endswith(".xlsx") or f.endswith(".xls"))
    ]

    # Define a custom key function to extract the number at the end of the filename
    def get_number(filename):
        return int(filename.split("_")[-1].split(".")[0])

    # Sort the files based on the number at the end of the filename
    files = sorted(files, key=get_number, reverse=True)

    errors = []

    data = pd.DataFrame()

    for filename in files:
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            ticker = filename.split("_")[1]
            try:
                df = pd.read_excel(os.path.join(directory, filename))

                # Reset and drop Indexes
                df = df.iloc[6:]
                df = df.iloc[:-3]  # Drop the "powered by fiintrade"
                df = df.reset_index(drop=True)
                # Tranpose and reset the index again
                df = df.transpose().reset_index(drop=True)
                # Set the first row as headers
                new_headers = df.iloc[0]
                df = df[1:]
                df.columns = new_headers
                df = df.rename(columns={"ITEMS": "Quarter"})
                # Add a new column named: "Ticker"
                df.insert(1, "Ticker", f"{ticker}")
                # df = df.iloc[::-1]

                data = pd.concat([data, df])
            except Exception as e:
                errors.append(e)
                print("Error: ", e)
                print("The number of errors:", len(errors))

    data = data.reset_index(drop=True)
    
    return data
