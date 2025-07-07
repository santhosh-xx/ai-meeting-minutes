import os
import gdown
import zipfile

def download_and_extract_model_zip():
    file_id = "1UJ98vSunCJRHQU9P3HlDL4H66uPvEINi"
    zip_path = "models.zip"
    extract_path = "models"

    # Skip if already downloaded
    if os.path.exists(extract_path):
        print("✅ Models folder already exists.")
        return

    url = f"https://drive.google.com/uc?id={file_id}"

    print("⬇️ Downloading models.zip from Google Drive...")
    gdown.download(url, zip_path, quiet=False)

    print("📦 Extracting zip file...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    print("🧹 Cleaning up zip file...")
    os.remove(zip_path)

    print("✅ Models are ready at ./models")

if __name__ == "__main__":
    download_and_extract_model_zip()
