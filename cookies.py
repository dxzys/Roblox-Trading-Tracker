import aiohttp
import asyncio
from pathlib import Path

async def check_pair(session, proxy, cookie, pair_id, pairs_file_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        async with session.get(
            "https://users.roblox.com/v1/users/authenticated", 
            headers=headers, 
            cookies={'.ROBLOSECURITY': cookie},
            proxy=f"http://{proxy}",
            timeout=10
        ) as response:
            if response.status == 401:
                print(f"Pair {pair_id} is invalid. Removing from list.")
                remove_bad_pair(proxy, cookie, pairs_file_path)
                return None
                
            user_data = await response.json()
            username = user_data.get('name', 'Unknown User')
            print(f"Pair {pair_id} works! User: {username}")
            return (f"Pair {pair_id}", proxy, cookie)
            
    except Exception as e:
        print(f"Error with pair {pair_id}: {str(e)}")
        remove_bad_pair(proxy, cookie, pairs_file_path)
        return None

def remove_bad_pair(bad_proxy, bad_cookie, pairs_file_path):
    with open(pairs_file_path, 'r') as file:
        all_pairs = file.read().splitlines()
    
    all_pairs = [pair for pair in all_pairs if pair != f"{bad_proxy}/{bad_cookie}"]
    
    with open(pairs_file_path, 'w') as file:
        file.write('\n'.join(all_pairs))

def load_pairs_from_file(file_path):
    path = Path(file_path)
    
    if not path.exists():
        print(f"Error: Can't find file '{file_path}'")
        return []
        
    with open(path, 'r') as file:
        pairs = [line.strip().split('/', 1) for line in file.readlines() if line.strip()]
    
    print(f"Loaded {len(pairs)} proxy/cookie pairs")
    return pairs

async def validate_all_pairs(pairs, pairs_file_path):
    if not pairs:
        print("No proxy/cookie pairs found to check.")
        return []
        
    print(f"Starting validation of {len(pairs)} pairs...")
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            check_pair(session, proxy, cookie, i, pairs_file_path) 
            for i, (proxy, cookie) in enumerate(pairs, start=1)
        ]
        results = await asyncio.gather(*tasks)
    
    return [result for result in results if result]

def main():
    script_dir = Path(__file__).parent.absolute()
    txts_dir = script_dir / "txts"
    pairs_file = txts_dir / "proxy_cookie_pairs.txt"

    pairs = load_pairs_from_file(pairs_file)
    valid_pairs = asyncio.run(validate_all_pairs(pairs, pairs_file))

    if not valid_pairs:
        print("No valid proxy/cookie pairs found.")
    else:
        print(f"\nFound {len(valid_pairs)} valid proxy/cookie pairs:")
        for pair in valid_pairs:
            print(f"{pair[0]}: Proxy: {pair[1]}, Cookie: {pair[2]}")

if __name__ == "__main__":
    main()
