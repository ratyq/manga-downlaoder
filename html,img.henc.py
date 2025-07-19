import os
import requests
from bs4 import BeautifulSoup

# إعداد المجلدات
if not os.path.exists("pages"):
    os.makedirs("pages")
if not os.path.exists("images"):
    os.makedirs("images")

# تحميل الصفحات
def download_pages(base_url, start, end):
    for i in range(start, end + 1):
        page_num = str(i).zfill(2)  # صيغة الرقم بصفرين (00, 01, ...)
        url = f"{base_url}{page_num}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Downloading: {url}")
            with open(f"pages/page_{page_num}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
        else:
            print(f"Failed to download: {url}")

# استخراج الصور من الصفحات
def extract_images():
    global_image_counter = 1  # عداد الصور للتسلسل
    for file_name in os.listdir("pages"):
        if file_name.endswith(".html"):
            with open(f"pages/{file_name}", "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                images = soup.find_all("img")
                for img in images:
                    img_url = img.get("src")
                    if img_url:
                        try:
                            response = requests.get(img_url, stream=True)
                            if response.status_code == 200:
                                # اسم الصورة بالتسلسل
                                img_extension = os.path.splitext(img_url)[1]
                                img_name = f"image_{str(global_image_counter).zfill(4)}{img_extension}"
                                img_path = f"images/{img_name}"
                                with open(img_path, "wb") as img_file:
                                    img_file.write(response.content)
                                print(f"Downloaded image: {img_name}")
                                global_image_counter += 1
                        except Exception as e:
                            print(f"Error downloading {img_url}: {e}")

# إعداد الرابط الأساسي والبداية والنهاية
base_url = "https://lekmanga.net/manga/master-of-gu/"
start_page = 0
end_page = 96

# تنفيذ العمليات
download_pages(base_url, start_page, end_page)
extract_images()
