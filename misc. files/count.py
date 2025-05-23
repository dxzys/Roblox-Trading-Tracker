# This was used to count the number of UAIDs I had logged for a particular limited ID, if any records existed in the uaidLog folder.
# Only works properly if you move this to the main project folder and run it from there.
import os
from pathlib import Path

def count_uaids(log_folder, limited_id):
    json_file_path = log_folder / f"{limited_id}.json"
    if not json_file_path.exists():
        print(f"No log file found for limited: {limited_id}")
        return
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    uaid_count = 0
    for entry in data.values():
        uaid_count += len(entry)
    print(f"Number of UAIDs logged for limited {limited_id}: {uaid_count}")

def main():
    limited_id = input("Enter the limited ID: ")
    main_project_folder = Path(__file__).parent.absolute()
    log_folder = main_project_folder / 'uaidLog'
    count_uaids(log_folder, limited_id)

if __name__ == "__main__":
    main()
