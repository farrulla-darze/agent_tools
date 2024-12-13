import os
import PyPDF2

class PDFIngestor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def ingest(self):
        documents = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.folder_path, filename)
                text = self.extract_text_from_pdf(file_path)
                metadata = {"filename": filename}
                document = Document(page_content=text, metadata=metadata)
                documents.append(document)
                self.save_to_txt(text, filename)
        return documents

    def extract_text_from_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.getPage(page_num).extractText()
        return text

    def save_to_txt(self, text, filename):
        output_folder = "output_txt"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_path, "w") as f:
            f.write(text)

class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata


if __name__ == '__main__':
    folder_path = "/home/joao/NP-Labs/demo/Klabin/Central de Resultados"
    if not os.path.exists(folder_path):
        print(f"Invalid path: {folder_path}")
        exit()

    print(f"Ingesting documents from {folder_path}...")
    pdf_ingester = PDFIngestor(folder_path)
    documents = pdf_ingester.ingest()
    print("Documents ingested successfully!")