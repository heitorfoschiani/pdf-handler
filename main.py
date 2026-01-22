from pdf_extractor import PDFExtractor


PDF_FILE_PATH = r""


if __name__ == "__main__":    
    pdf_extractor = PDFExtractor(PDF_FILE_PATH)
    pdf_contents = pdf_extractor.extract_contents()
    pdf_contents.sort()
    pdf_contents.join()
