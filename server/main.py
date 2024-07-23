import OCR

if __name__ == '__main__':
    tess_path = '/usr/bin/tesseract'
    view_mode = 3
    source = 0
    crop = [0, 0]
    language = "eng"
    OCR.tesseract_location(tess_path)
    OCR.ocr_stream(view_mode=view_mode, source=source, crop=crop, language=language)