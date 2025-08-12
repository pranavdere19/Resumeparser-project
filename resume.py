import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber
import re
import os

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def extract_email(text):
    match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match[0] if match else "Not found"

def extract_phone(text):
    # Match mobile numbers: 10-digit or with +91, allow space/hyphen
    match = re.findall(r"(\+91[\-\s]?\d{10}|\b\d{10}\b)", text)
    return match[0] if match else "Not found"

def extract_name(text):
    lines = text.strip().split('\n')
    return lines[0] if lines else "Not found"

def extract_skills(text):
    keywords = ['python', 'java', 'html', 'css', 'django', 'react', 'mysql']
    found = [word for word in keywords if word.lower() in text.lower()]
    return ', '.join(set(found)) if found else "Not found"

def parse_resume():
    filepath = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Choose a Resume PDF"
    )

    if not filepath:
        return

    if not os.path.exists(filepath):
        messagebox.showerror("Error", "File not found.")
        return

    try:
        text = extract_text_from_pdf(filepath)
        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)

        result_text.set(f"👤 Name:   {name}\n📧 Email:  {email}\n📞 Phone:  {phone}\n🛠️  Skills: {skills}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI SETUP ===
root = tk.Tk()
root.title("Resume Parser App")
root.geometry("500x300")

tk.Label(root, text="📄 Resume Parser", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Upload and Parse PDF", command=parse_resume).pack(pady=10)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, justify="left", wraplength=450, font=("Arial", 12)).pack(pady=20)

root.mainloop()