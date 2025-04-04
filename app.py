from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CLEANED_FOLDER = 'cleaned'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEANED_FOLDER, exist_ok=True)

def clean_data(input_path, output_path):
    # Basic cleaning operations
    df = pd.read_csv(input_path)
    
    # 1. Remove duplicate rows
    df = df.drop_duplicates()
    
    # 2. Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 3. Convert string columns to proper case
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.title()
    
    # 4. Save cleaned data
    df.to_csv(output_path, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_path = os.path.join(CLEANED_FOLDER, f'cleaned_{file.filename}')
            file.save(input_path)
            clean_data(input_path, output_path)
            return send_file(output_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
