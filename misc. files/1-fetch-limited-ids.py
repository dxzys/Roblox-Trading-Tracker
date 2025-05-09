# this just gets all of the limiteds from the rolimons itemdetails api and saves them to a txt file for pre-loading use.
# it's just easier to get (at least most) the limiteds instead of having to manually get the limited IDs.
import requests
from pathlib import Path

def get_limited_ids():
    url = "https://www.rolimons.com/itemapi/itemdetails"
    try:
        print("Fetching limited items from Rolimons...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("success"):
            print("Rolimons API reported failure in the response")
            return []

        limited_ids = list(data["items"].keys())
        print(f"Found {len(limited_ids)} limited items")
        return limited_ids

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except ValueError:
        print("Error parsing JSON response")
        return []

def save_ids_to_file(limited_ids):
    if not limited_ids:
        print("No limited IDs to save")
        return
    
    script_dir = Path(__file__).parent.absolute()
    txts_dir = script_dir / "txts"
    
    txts_dir.mkdir(exist_ok=True)
    
    file_path = txts_dir / "limiteds.txt"
    
    with open(file_path, "w") as file:
        for item_id in limited_ids:
            file.write(f"{item_id}\n")
    
    print(f"Saved {len(limited_ids)} limited IDs to {file_path}")

def main():
    limited_ids = get_limited_ids()
    
    if limited_ids:
        save_ids_to_file(limited_ids)
    else:
        print("Failed to get limited IDs.")

if __name__ == "__main__":
    main()
