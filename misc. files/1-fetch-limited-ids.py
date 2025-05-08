# this just gets all of the limiteds from the rolimons itemdetails api and saves them to a txt file for pre-loading use.
# it's just easier to get (at least most) the limiteds instead of having to manually get the limited IDs.
import requests
import os

def fetch_limited_ids():
    url = "https://www.rolimons.com/itemapi/itemdetails"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            limited_ids = data["items"].keys()
            save_limited_ids_to_file(limited_ids)
        else:
            print("Failed to retrieve item details.")
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

def save_limited_ids_to_file(limited_ids):
    project_location = os.path.dirname(os.path.abspath(__file__))
    txts_dir = os.path.join(project_location, "txts")
    
    if not os.path.exists(txts_dir):
        os.makedirs(txts_dir)
    
    file_path = os.path.join(txts_dir, "limiteds.txt")
    
    with open(file_path, "w") as file:
        for item_id in limited_ids:
            file.write(f"{item_id}\n")
    
    print(f"Limited IDs saved to {file_path}")

if __name__ == "__main__":
    fetch_limited_ids()
