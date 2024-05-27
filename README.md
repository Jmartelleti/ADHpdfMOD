PDF Word Highlighter

This Python script aims to enhance reading experience and concentration by highlighting the first two letters of each word in a PDF document. Text modification in the PDF is done in a way that the first two letters of each word are bolded, while the rest of the text remains unchanged. This technique is intended to help readers quickly grasp the structure and meaning of key words in the text, which can be especially usef l for individuals with Attention Deficit Hyperactivity Disorder (ADHD) or other concentration challenges.

How it Works
The script takes a PDF file as input and processes each page of the document. For each page, it extracts text and images using the pdfplumber library. It then highlights the first two letters of each word in bold and preserves the rest of the text unchanged. Additionally, it retains the original images from the PDF. The modified document is saved as a new PDF file.

Usage Instructions

  ->Install the required dependencies by running pip install pdfplumber
  reportlab Pillow.

  ->Run the script providing the path of the PDF file
  you want to modify.

  ->The script will generate a new PDF file with the
  modifications applied.

  ->Example bash Copiar código python word_highlighter.py input_file.pdf

Notes

This script is designed to enhance readability and concentration by highlighting the first two letters of each word in a PDF document. However, results may vary depending on the content and format of the original PDF. It may be necessary to adjust the size and position of images in the modified document to ensure proper presentation.
