from PIL import Image
import os

def images_to_pdf(images_folder, output_file="output.pdf"):
    if not os.path.exists(images_folder):
        print("The specified folder does not exist!")
        return
    
    images = sorted(
        [img for img in os.listdir(images_folder) if img.endswith((".png", ".jpg", ".jpeg"))],
        key=lambda img: os.path.getctime(os.path.join(images_folder, img))
    )
    
    if not images:
        print("No images found in the specified folder!")
        return

    pdf_images = []
    for img_file in images:
        img_path = os.path.join(images_folder, img_file)
        try:
            img = Image.open(img_path)
            
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            pdf_images.append(img)
        except Exception as e:
            print(f"Error processing the image {img_file}: {e}")
    
    if pdf_images:
        pdf_images[0].save(
            output_file,
            save_all=True,
            append_images=pdf_images[1:]
        )
        print(f"PDF successfully created: {output_file}")
    else:
        print("No valid images found to create a PDF.")

images_folder = input("Enter the path to the folder containing the images: ").strip()
output_file = input("Enter the name of the PDF file to create (default is example.pdf): ").strip()

if not output_file:
    output_file = "example.pdf"

images_to_pdf(images_folder, output_file)
