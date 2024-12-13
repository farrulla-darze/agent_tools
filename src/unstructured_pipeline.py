import os
import logging
from unstructured.partition.pdf import partition_pdf
import pdfplumber

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class UnstructuredIngest:
    def __init__(self, documents_path, debug=False, index_debug : int = 0):
        self.documents_path = documents_path
        self.debug = debug
        self.index_debug = index_debug  # Index of the document to debug (0-indexed)

    def ingest(self):
        documents = os.listdir(self.documents_path)
        
        # Debug mode: only process the first document
        if self.debug:
            documents = [documents[self.index_debug]]  # Only process the first document
        
        for filename in documents:
            file_path = os.path.join(self.documents_path, filename)
            logging.info(f"Processing file: {file_path}")
            self.extract_elements(file_path)

    def extract_elements(self, file_path):
        try:
            elements = partition_pdf(file_path)
            logging.debug(f"Extracted elements: {elements}")
        except Exception as e:
            logging.error(f"Failed to process {file_path}: {e}")
        
    def select_strategy(self, file_path):
        """
        Selects the best strategy to use for processing the document based on its characteristics.
        """
        if self.has_table(file_path):
            strategy = "hi_res"
        elif self.has_extractable_text(file_path):
            strategy = "ocr_only"
        else:
            strategy = "auto"
        logging.debug(f"Selected strategy for {file_path}: {strategy}")
    
    def has_table(self, file_path):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if len(page.find_tables(table_settings={})) > 0:
                    return True
        return False

    def has_extractable_text(self, file_path):
        # Placeholder function for checking text extractability
        return True

if __name__ == '__main__':
    path = 'Klabin/Central de Resultados'
    # 
    ingestor = UnstructuredIngest(path, debug=True, index_debug=0)
    ingestor.ingest()
