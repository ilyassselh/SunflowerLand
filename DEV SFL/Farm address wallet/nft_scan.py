import requests
import json
import sqlite3

api_key = "gbaKkb9iSo6ZCBpFLo7--HPVG3yrI55X"
address = "0x2b4a66557a79263275826ad31a4cddc2789334bd"
headers = {"accept": "application/json"}

tokenid = 1
commit_threshold = 10000  # Save data every 10,000 farms

# Connect to the SQLite database
conn = sqlite3.connect("nft_owners.db")
cursor = conn.cursor()

# Create a table to store the owners' data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS nft_owners (
        id INTEGER PRIMARY KEY,
        tokenid INTEGER,
        owner_address TEXT
    )
''')

while tokenid <= 165517:
    url = f"https://polygon-mainnet.g.alchemy.com/nft/v3/{api_key}/getOwnersForNFT?contractAddress={address}&tokenId={tokenid}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        owners = data['owners']
        
        # Save owners' data to the SQLite database
        for owner in owners:
            cursor.execute("INSERT INTO nft_owners (tokenid, owner_address) VALUES (?, ?)", (tokenid, owner))
            print(f"Farm ID: {tokenid}, Owner Address: {owner}")

        # Check if it's time to commit changes to the database
        if tokenid % commit_threshold == 0:
            conn.commit()
            print(f"Data saved for token IDs up to {tokenid}")

        if tokenid == 165517:
            print("Scan terminé")
            break
    else:
        print(f"Échec de récupération des données pour le token ID {tokenid}")

    tokenid += 1

# Commit any remaining changes to the database
conn.commit()

# Close the database connection when finished
conn.close()





