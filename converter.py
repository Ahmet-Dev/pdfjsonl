import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import json
import os
import asyncio
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

class PDFtoJSONLConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to JSONL Converter (Async & MultiThreaded)")
        self.root.geometry("500x350")

        self.label = tk.Label(root, text="PDF Dosyalarını JSONL'ye Dönüştür", font=("Arial", 12))
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="PDF Seç", command=self.select_pdfs, font=("Arial", 10))
        self.select_button.pack(pady=5)

        self.progress_label = tk.Label(root, text="", font=("Arial", 10))
        self.progress_label.pack(pady=5)

        self.progress = tk.Label(root, text="İlerleme: 0%", font=("Arial", 10))
        self.progress.pack()

        self.convert_button = tk.Button(root, text="Dönüştür", command=self.start_conversion, font=("Arial", 10))
        self.convert_button.pack(pady=10)

        self.output_label = tk.Label(root, text="", fg="green", font=("Arial", 10))
        self.output_label.pack(pady=5)

        self.pdf_files = []
        self.executor = ThreadPoolExecutor(max_workers=5)  # 5 paralel iş parçacığı

    def select_pdfs(self):
        """PDF dosyalarını seçmek için dosya seçme penceresi açar."""
        self.pdf_files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_files:
            messagebox.showinfo("Başarıyla Seçildi", f"{len(self.pdf_files)} PDF seçildi.")
        else:
            messagebox.showwarning("Uyarı", "PDF seçilmedi!")

    async def pdf_to_text(self, pdf_path):
        """PDF dosyasından metin çıkarma işlemi (async)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.extract_text_safe, pdf_path)

    def extract_text_safe(self, pdf_path):
        """Thread içinde çalışan, PDF'ten metin çıkaran yardımcı fonksiyon."""
        text = ""
        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                    else:
                        text += "[UYARI: Sayfa okunamadı]\n"
        except Exception as e:
            messagebox.showerror("Hata", f"PDF Okuma Hatası: {str(e)}")
        return text.strip()

    def clean_text(self, text):
        """Unicode karakterleri temizler ve hatalı karakterleri kaldırır."""
        return ''.join(c for c in text if unicodedata.category(c) != 'Cs')  # Surrogate karakterleri kaldır

    def split_text_to_sentences(self, text):
        """Metni cümlelere böler ve gereksiz boşlukları, kısa cümleleri temizler."""
        sentences = re.split(r'(?<=[.!?])\s+', text)  # Noktalama işaretlerinden sonra böler
        cleaned_sentences = [s.strip() for s in sentences if len(s.strip()) > 2]  # Boş veya çok kısa cümleleri filtrele
        return cleaned_sentences

    async def convert_pdfs_to_jsonl(self):
        """Seçilen tüm PDF'leri JSONL formatına çevirir, gereksiz cümleleri kaldırır."""
        if not self.pdf_files:
            messagebox.showwarning("Uyarı", "Lütfen en az bir PDF seçin!")
            return

        dataset = []
        total_files = len(self.pdf_files)

        for idx, pdf in enumerate(self.pdf_files):
            text = await self.pdf_to_text(pdf)
            text = self.clean_text(text)  # Unicode temizliği uygula
            sentences = self.split_text_to_sentences(text)

            for sentence in sentences:
                if len(sentence) > 2:  # Eğer cümle çok kısa değilse ekle
                    dataset.append({"text": sentence, "label": "Eğitim Verisi"})  

            progress = int(((idx + 1) / total_files) * 100)
            self.progress.config(text=f"İlerleme: {progress}%")
            self.root.update_idletasks()

        if dataset:
            output_file = "dataset.jsonl"
            with open(output_file, "w", encoding="utf-8", errors="ignore") as f:
                for entry in dataset:
                    if len(entry["text"]) > 2:  # Tekrar kontrol et, boş veya tek noktalama içerenleri ekleme
                        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

            self.output_label.config(text=f"JSONL başarıyla oluşturuldu: {output_file}")

    def start_conversion(self):
        """Dönüştürme işlemini başlatır (Thread içinde çalıştırılır)."""
        thread = Thread(target=lambda: asyncio.run(self.convert_pdfs_to_jsonl()))
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFtoJSONLConverter(root)
    root.mainloop()
