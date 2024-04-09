import os
import openai
import pytesseract
import fitz
from PIL import Image
from io import BytesIO
import docx
from flask import Flask, request, render_template

app = Flask(__name__)

openai.api_key = "api-key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', method=['POST'])
def process_file(self, *args):
    file_path = request.files['file'].filename
    question = request.form['question']

    text1 = convert_any_to_string(file_path)
    prompt = f"Given the following document {text1}\n\nAnswer the questions: {question}"
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    answer = response.choices[0].text.strip()
    return {'answer': answer}

def document_to_string(self, document_path, list_dict_final_images=None):
    _, file_extension = os.path.splitext(document_path)

    if file_extension.lower() in ['.png', '.jpeg', '.jpg']:
        image = Image.open(document_path)
        list_final_images = pytesseract.image_to_string(image)
        return list_final_images

    all_images = [list(data.values())[0] for data in list_dict_final_images]

    for index, image_bytes in enumerate(all_images):
        image = Image.open(BytesIO(image_bytes))
        figure = plt.figure(figsize=(image.width / 100, image.height / 100))

        plt.title(f"--- Page Number {index + 1} ---")
        plt.imshow(image)
        plt.axis("off")
        plt.show()

def pdf_to_image(self, file_path, scale=300 / 72):
    text = ""
    pdf_document = fitz.open(file_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()
    return text

def png_to_string(self, filepath):
    try:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error converting PNG to string: {e}")
        return None

def txt_to_string(self, filepath):
    try:
        with open(filepath, 'r') as file:
            text = file.read()
        return text
    except Exception as e:
        print(f"Error converting TXT to string: {e}")
        return None

def docx_to_string(self, filepath):
    try:
        doc = docx.Document(filepath)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error converting DOCX to string: {e}")
        return None

def convert_any_to_string(self, filepath):
    my_path = filepath
    if my_path.endswith(".pdf"):
        return self.pdf_to_image(my_path)
    elif my_path.endswith(".png"):
        return self.png_to_string(my_path)
    elif my_path.endswith(".jpeg"):
        return self.document_to_string(my_path)
    elif my_path.endswith(".txt"):
        return self.txt_to_string(my_path)
    elif my_path.endswith(".docx"):
        return self.docx_to_string(my_path)
    elif my_path.endswith(".jpg"):
        return self.document_to_string(my_path)
    else:
        return "The extension is not valid!"

if __name__ == '__main__':
    app.run(debug=Ture)
