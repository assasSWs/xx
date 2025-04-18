import pandas as pd
import requests
import time
import os

# Function to download files from URL
def download_files_from_url(csv_path, download_dir):
    # Create download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)
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
                # Extract name and ID
                name = str(row[0]).strip()
                id_number = str(row[1]).strip()
                
                # Create a subfolder for this person
                person_folder = os.path.join(download_dir, name)
                os.makedirs(person_folder, exist_ok=True)
                
                print(f"Processing {index+1}/{len(df)}: {name} (ID: {id_number})")
                
                # Download each file type
                for file_type in file_types:
                    # URL with the ID and file type
                    url = f"https://mis.kln.ac.lk/storage/files/2021/{id_number}/{file_type}"
                    
                    # Output filename
                    output_filename = f"{name}_{file_type}"
                    output_path = os.path.join(person_folder, output_filename)
                    
                    print(f"  Downloading {file_type} from {url}")
                    
                    try:
                        # Download the file
                        response = requests.get(url, stream=True)
                        response.raise_for_status()  # Raise an error for bad responses
                        
                        # Save to directory
                        with open(output_path, "wb") as file:
                            for chunk in response.iter_content(chunk_size=8192):
                                file.write(chunk)
                        
                        print(f"    Success: Saved to {output_filename}")
                        successful_downloads += 1
                        
                    except requests.exceptions.RequestException as e:
                        print(f"    Download failed for {file_type}: {e}")
                        failed_downloads += 1
                    
                    # Add a small delay to avoid overwhelming the server
                    time.sleep(1)
                
            except Exception as e:
                print(f"  Error processing {name}: {e}")
                failed_downloads += 1
        
        # Summary
        print("\nDownload Summary:")
        print(f"Total entries: {len(df)}")
        print(f"Expected total files: {len(df) * len(file_types)}")
        print(f"Successfully downloaded: {successful_downloads}")
        print(f"Failed downloads: {failed_downloads}")
        print(f"All files saved to: {download_dir}")
        
    except FileNotFoundError:
        print(f"Error: The file {csv_path} was not found.")
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")

# Main execution
if __name__ == "__main__":
    # Set paths
    csv_path = "bs.csv"  # Path to your CSV file
    download_dir = "./downloaded_files"  # Directory where files will be downloaded
    
    # Install pandas and requests if not already installed
    try:
        import pandas
        import requests
    except ImportError:
        print("Installing required packages...")
        os.system("pip install pandas requests")
    
    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"File {csv_path} not found. Please ensure it's in the current directory.")
        exit()
    
    # Download files
    download_files_from_url(csv_path, download_dir)
