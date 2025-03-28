from paddleocr import PaddleOCR

def pdf_to_text(pdf_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    result = ocr.ocr(pdf_path, cls=True)
    
    text_content = []
    for page in result:
        for line in page:
            if line and len(line) >= 2:  # 确保有有效结果
                text_content.append(line[1][0])
    
    return '\n'.join(text_content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(pdf_to_text(pdf_path))
    else:
        print("请提供PDF文件路径作为参数")
