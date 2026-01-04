import gdown
import sys
import re
import os

def is_folder_link(url: str) -> bool:
    return bool(re.search(r"/folders/", url))

def download_from_google_drive(url, output=None):
    try:
        if is_folder_link(url):
            print("Detected Google Drive folder.")
            if output is None:
                output = "gdrive_folder"
            os.makedirs(output, exist_ok=True)

            gdown.download_folder(
                url=url,
                output=output,
                quiet=False,
                use_cookies=True
            )
        else:
            print("Detected Google Drive file.")
            gdown.download(
                url,
                output=output,
                quiet=False,
                fuzzy=True
            )

    except Exception as e:
        print("Download failed:", e)
        sys.exit(1)
if __name__ == "__main__":
    link = "https://docs.google.com/spreadsheets/d/1_m83EXeUr0ZboZrWPEpjB6lAzSxVIq0XyugKENt72nQ/edit?usp=sharing"
    output = "people.xlsx"
    download_from_google_drive(link, output)
    link2  ='https://drive.google.com/drive/folders/1-qqMJcdzORG0ncGZQ8JyV-fpV-5rSgZPQ9jYJo3vmKs7CqIsd0TXm_Lefi9utJl4RMavdbnX?usp=drive_link'
    output2 = 'people_photos'
    download_from_google_drive(link2, output2)