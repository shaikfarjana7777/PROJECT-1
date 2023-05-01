from flask import Flask,request,jsonify, render_template
from PIL import Image
import pytesseract
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Adhar.html")

@app.route('/ocr', methods=[ 'POST'])
def ocr():
    
    image_file = request.files['file']

    image = Image.open(image_file)

    text = pytesseract.image_to_string(image)

    aadhaar_regex = r"\d{4} \d{4} \d{4}"
    name_regex = r"\|\s+([A-Za-z ]+)\n"
    address_regex = r"Address: ((?:.+\n)+(?<=\n)[\w\s]+[^\n\d]+[^\n]+\d{6})"
    dob_regex = r"DOB: (\d{2}/\d{2}/\d{4})"

    aadhaar_match = re.search(aadhaar_regex, text)
    name_match = re.search(name_regex, text)
    address_match = re.search(address_regex, text)
    dob_match = re.search(dob_regex, text)

    if aadhaar_match:
        aadhaar_number = aadhaar_match.group(0)
    else:
        aadhaar_number = "No Aadhaar number found."

    if name_match:
        name = name_match.group(1)
    else:
        name = "No name found."

    if address_match:
        address = address_match.group(1)
    else:
        address = "No address found."

    if dob_match:
        dob = dob_match.group(1)
    else:
        dob = "No DOB found."

    response_data = {
        'aadhaar_number': aadhaar_number,
        'name': name,
        'address': address,
        'dob': dob
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
