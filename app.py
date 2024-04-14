import pandas as pd
import subprocess
import urllib.request
import os
import joblib
import zipfile

def process_chemical_data(file_path):
    print("All the modules are imported successfully!...")

    # Download padel.zip using urllib.request
    url_zip = 'https://github.com/dataprofessor/bioinformatics/raw/master/padel.zip'
    urllib.request.urlretrieve(url_zip, 'padel.zip')
    print("padel.zip downloaded successfully.")

    # Download padel.sh using urllib.request
    url_sh = 'https://github.com/dataprofessor/bioinformatics/raw/master/padel.sh'
    urllib.request.urlretrieve(url_sh, 'padel.sh')
    print("padel.sh downloaded successfully.")

    # Unzip padel.zip
    with zipfile.ZipFile('padel.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    print("padel.zip extracted successfully.")

    # Taking input for prediction
    df3 = pd.read_csv('input.csv')
    print("input.csv read!..")
    print(df3)

    print("Selecting the attributes....")
    # Selecting the attributes
    selection = ['canonical_smiles','molecule_chembl_id']
    df3_selection = df3[selection]
    df3_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)

    print("molecule.smi created successfully.")

    # Print first 5 lines of molecule.smi
    with open('molecule.smi', 'r') as file:
        print("First 5 lines of molecule.smi:")
        for i in range(5):
            print(file.readline().strip())

    # Count the number of lines in molecule.smi
    num_lines = sum(1 for line in open('molecule.smi'))
    print("Number of lines in molecule.smi:", num_lines)

    # Print the content of padel.sh
    with open('padel.sh', 'r') as file:
        print("Content of padel.sh:")
        print(file.read())

    # Define the command to execute
    command = [
        'java', '-Xms1G', '-Xmx1G', '-Djava.awt.headless=true',
        '-jar', './PaDEL-Descriptor/PaDEL-Descriptor.jar',
        '-removesalt', '-standardizenitro', '-fingerprints',
        '-descriptortypes', './PaDEL-Descriptor/PubchemFingerprinter.xml',
        '-dir', './', '-file', 'descriptors_output.csv'
    ]

    # Execute the command
    print("Executing padel.sh script...")
    try:
        subprocess.run(command, shell=True, check=True)
        print("Padel.sh script executed successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing padel.sh script:", e)

    # Check if descriptors_output.csv file is created
    if os.path.exists('descriptors_output.csv'):
        print("Descriptors output file created successfully.")
        # Read descriptors output
        df3_X = pd.read_csv('descriptors_output.csv')
        print("Descriptors read:")
        print(df3_X)
    else:
        print("Descriptors output file not found. Check the execution of padel.sh script.")

    print("Descriptors calculated.")

    # Read descriptors output
    df3_X = pd.read_csv('descriptors_output.csv')
    print("Descriptors read:")
    print(df3_X)

    print("Load the trained model from the .pkl file")
    # Load the trained model from the .pkl file
    model_info = joblib.load('model.pkl')
    loaded_model = model_info['model']

    print("Read the selected column names from the text file")
    # Read the selected column names from the text file
    selected_column_names_txt = 'selected_column_names.txt'
    with open(selected_column_names_txt, 'r') as file:
        selected_column_names = [line.strip() for line in file]

    print("Filtering the DataFrame to keep only the selected columns")

    # Filter the DataFrame to keep only the selected columns
    df_selected = df3_X[selected_column_names]
    print("#" * 100)
    print("Predicting the output!....")
    Y_pred = loaded_model.predict(df_selected)
    print("Predictions:")
    print(Y_pred)

    Y_pred = pd.DataFrame(Y_pred, columns=["Prediction"])

    print("Output:")
    Output = pd.concat([df3_X, Y_pred], axis=1)
    print(Output)

    #return Output
    # Process the DataFrame (example: convert to HTML string)
    html_string1 = Output.to_html()
    html_string2 = Y_pred.to_html()
    
    # Return the HTML string
    return html_string1, html_string2


from flask import Flask, render_template, request

app = Flask(__name__)


# Define route for the upload form
@app.route('/')
def upload_form():
    return render_template('index.html')


# Define route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'

        # If the file is present and has a valid filename
        if file:
            # Save the file to a temporary location
            #'/tmp/' +
            file_path = file.filename
            file.save(file_path)

            # Call process_chemical_data with the file path
            result = process_chemical_data(file_path)

            # Return the result or render a template with the result
            return result


# Function to process the uploaded file
'''def process_chemical_data(file_path):
    # Call your function to process the chemical data with the file_path
    # For example:
    # result = your_function(file_path)
    result = f'Processing chemical data with file: {file_path}'
    return result'''


if __name__ == '__main__':
    app.run(debug=True)
