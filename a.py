import pandas as pd
import requests
import time
import os

# Function to check if file exists at URL
def file_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except:
        return False

# Function to download files from URL
def download_files_from_url(csv_path, download_dir):
    print(f"Files will be downloaded to: {download_dir}")
    
    # Define the file types to download for each ID
    file_types = ["nee1.pdf", "asss.pdf", "aa.pdf"]
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_path, header=None)
        print(f"Found {len(df)} rows in the CSV file.")
        
        # Process each row
        successful_downloads = 0
        failed_downloads = 0
        
        for index, row in df.iterrows():
            try:
                name = str(row[0]).strip()
                id_number = str(row[1]).strip()
                print(f"Processing {index+1}/{len(df)}: {name} (ID: {id_number})")

                files_downloaded = 0
                temp_files = []

                for file_type in file_types:
                    url = f"https://mis.kln.ac.lk/storage/files/2023/{id_number}/{file_type}"
                    output_filename = f"{name}_{file_type}"
                    output_path = os.path.join(download_dir, name, output_filename)

                    print(f"  Checking {file_type} from {url}")
                    
                    try:
                        response = requests.get(url, stream=True, timeout=10)
                        if response.status_code == 200:
                            temp_files.append((output_path, response))
                            files_downloaded += 1
                        else:
                            print(f"    Not found: {file_type}")
                            failed_downloads += 1
                    except requests.exceptions.RequestException as e:
                        print(f"    Request failed for {file_type}: {e}")
                        failed_downloads += 1
                    
                    time.sleep(1)

                if files_downloaded > 0:
                    person_folder = os.path.join(download_dir, name)
                    os.makedirs(person_folder, exist_ok=True)
                    for output_path, response in temp_files:
                        with open(output_path, "wb") as file:
                            for chunk in response.iter_content(chunk_size=8192):
                                file.write(chunk)
                        print(f"    Saved: {os.path.basename(output_path)}")
                        successful_downloads += 1
                else:
                    print(f"    No files found for {name} (ID: {id_number})")

            except Exception as e:
                print(f"  Error processing {name}: {e}")
                failed_downloads += 1
        
        # Summary
        print("\nDownload Summary:")
        print(f"Total entries: {len(df)}")
        print(f"Expected total files: {len(df) * len(file_types)}")
        print(f"Successfully downloaded: {successful_downloads}")
        print(f"Failed downloads: {failed_downloads}")
        
    except FileNotFoundError:
        print(f"Error: The file {csv_path} was not found.")
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")

# Main execution
if __name__ == "__main__":
    csv_path = "bs.csv"
    download_dir = "./downloaded_files"

    if not os.path.exists(csv_path):
        print(f"File {csv_path} not found. Please ensure it's in the current directory.")
        exit()
    
    download_files_from_url(csv_path, download_dir)
