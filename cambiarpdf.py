import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import tkinter as tk
from tkinter import filedialog, messagebox
import tempfile
import os

def extract_text_and_images_from_pdf(pdf_path):
    pages_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            images = []
            for img in page.images:
                img_bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
                with pdfplumber.open(pdf_path) as temp_pdf:
                    temp_page = temp_pdf.pages[page.page_number - 1]
                    cropped_image = temp_page.within_bbox(img_bbox).to_image()
                    img_stream = BytesIO()
                    cropped_image.save(img_stream, format="PNG")
                    img_stream.seek(0)
                    images.append((img_stream, img_bbox))
            pages_data.append((text, images, page.bbox))
    return pages_data

def bold_first_two_letters(text):
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        words = line.split()
        new_words = []
        for word in words:
            if len(word) > 2:
                new_word = f"<b>{word[:2]}</b>{word[2:]}"
            else:
                new_word = f"<b>{word}</b>"
            new_words.append(new_word)
        new_lines.append(' '.join(new_words))
    return '\n'.join(new_lines)

def create_pdf_with_bold_text_and_images(pages_data, output_path):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 12)

    try:
        for page_index, (text, images, bbox) in enumerate(pages_data):
            bold_text = bold_first_two_letters(text)
            lines = bold_text.split('\n')
            y = bbox[3] - 50  # Start at the top of the page

            # Draw text
            for line in lines:
                if y < 50:  # Add a new page if needed
                    can.showPage()
                    y = bbox[3] - 50
                x = 50  # Reset x to left margin
                for word in line.split(' '):
                    if word.startswith('<b>'):
                        bold_word = word.replace('<b>', '').replace('</b>', '')
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(x, y, bold_word[:2])
                        x += can.stringWidth(bold_word[:2], "Helvetica-Bold", 12)
                        can.setFont("Helvetica", 12)
                        can.drawString(x, y, bold_word[2:])
                        x += can.stringWidth(bold_word[2:], "Helvetica", 12)
                    else:
                        can.drawString(x, y, word)
                        x += can.stringWidth(word, "Helvetica", 12)
                    x += can.stringWidth(' ', "Helvetica", 12)  # Add space between words
                y -= 14  # Move to the next line

            # Draw images
            for img_stream, img_bbox in images:
                img_reader = ImageReader(img_stream)
                img_width = img_bbox[2] - img_bbox[0]
                img_height = img_bbox[3] - img_bbox[1]
                can.drawImage(img_reader, img_bbox[0], bbox[3] - img_bbox[1] - img_height, width=img_width, height=img_height)
            
            can.showPage()  # Move to a new page for the next set of text and images

        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        with open(output_path, 'wb') as f:
            f.write(packet.getvalue())

        return len(pages_data)
    finally:
        pass  # Ensure all resources are cleaned up

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    input_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if input_pdf_path:
        output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_pdf_path:
            pages_data = extract_text_and_images_from_pdf(input_pdf_path)
            generated_pages = create_pdf_with_bold_text_and_images(pages_data, output_pdf_path)
            total_pages = len(pages_data)
            if total_pages == generated_pages:
                messagebox.showinfo("Proceso Completado", f"El PDF se ha guardado en {output_pdf_path} con {generated_pages} páginas.")
            else:
                messagebox.showwarning("Advertencia", f"El PDF original tiene {total_pages} páginas, pero el PDF generado tiene {generated_pages} páginas. Por favor, verifique el archivo.")

if __name__ == "__main__":
    main()
