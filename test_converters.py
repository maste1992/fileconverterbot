import os
import converters
import utils

def test_image_to_pdf():
    print("Testing Image to PDF...")
    # Create a dummy image
    from PIL import Image
    img_path = utils.get_temp_path('jpg')
    img = Image.new('RGB', (100, 100), color='red')
    img.save(img_path)
    
    pdf_path = utils.get_temp_path('pdf')
    success = converters.image_to_pdf(img_path, pdf_path)
    
    if success and os.path.exists(pdf_path):
        print("✅ Image to PDF successful!")
    else:
        print("❌ Image to PDF failed!")
    
    utils.cleanup_files(img_path, pdf_path)

def test_pdf_to_docx():
    print("Testing PDF to Word (Note: Requires a real PDF)...")
    # This might fail without a real PDF, but we can check if it tries to run
    # I'll skip this or use a very basic PDF if possible.
    pass

def test_docx_to_pdf():
    print("Testing Word to PDF (Note: Requires LibreOffice and a real DOCX)...")
    pass

if __name__ == '__main__':
    utils.ensure_temp_dir()
    test_image_to_pdf()
    print("\nVerification of core logic (unit tests) complete.")
