#Import libraries
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import joblib
import subprocess
import urllib.request

print("All the modules are imported successfully!...")

# Download padel.zip using urllib.request
url_zip = 'https://github.com/dataprofessor/bioinformatics/raw/master/padel.zip'
urllib.request.urlretrieve(url_zip, 'padel.zip')
print("padel.zip downloaded successfully.")

# Download padel.sh using urllib.request
url_sh = 'https://github.com/dataprofessor/bioinformatics/raw/master/padel.sh'
urllib.request.urlretrieve(url_sh, 'padel.sh')
print("padel.sh downloaded successfully.")


#! wget https://github.com/dataprofessor/bioinformatics/raw/master/padel.zip
#! wget https://github.com/dataprofessor/bioinformatics/raw/master/padel.sh
subprocess.run(['unzip', 'padel.zip'])
print("subprocess command are executed..")
#! unzip padel.zip
print("subprocess command are executed..")
#taking input for prediction
df3 = pd.read_csv('input.csv')

print("input.csv read!..")
print(df3)

print("selecting the attributes....")
#selecting the attributes
selection = ['canonical_smiles','molecule_chembl_id']
df3_selection = df3[selection]
df3_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)

'''! cat molecule.smi | head -5

! cat molecule.smi | wc -l

! cat padel.sh'''

# Print first 5 lines of molecule.smi
result_head = subprocess.run(['cat', 'molecule.smi'], stdout=subprocess.PIPE)
print(result_head.stdout.decode('utf-8').split('\n')[:5])
print("subprocess command are executed..")

# Count the number of lines in molecule.smi
result_wc = subprocess.run(['cat', 'molecule.smi', '|', 'wc', '-l'], stdout=subprocess.PIPE, shell=True)
print(result_wc.stdout.decode('utf-8'))
print("subprocess command are executed..")

# Print the content of padel.sh
result_padel = subprocess.run(['cat', 'padel.sh'], stdout=subprocess.PIPE)
print(result_padel.stdout.decode('utf-8'))
print("subprocess command are executed..")



#predicting the padel descriptors
#! bash padel.sh


# Execute padel.sh script
result_padel = subprocess.run(['bash', 'padel.sh'], stdout=subprocess.PIPE)
print(result_padel.stdout.decode('utf-8'))
print("subprocess command are executed..")

print("Reading descriptors ")
df3_X = pd.read_csv('descriptors_output.csv')
print(df3_X)

x1 = df3_X.drop('Name', axis=1)
print(x1)

print('Load the trained model from the .pkl file')
# Load the trained model from the .pkl file
model = joblib.load('model.pkl')

print("Read the selected column names from the text file")
# Read the selected column names from the text file
selected_column_names_txt = 'selected_column_names.txt'
with open(selected_column_names_txt, 'r') as file:
    selected_column_names = [line.strip() for line in file]

print("reading descriptors")
# Read the original DataFrame
df = pd.read_csv('descriptors_output.csv')

print("Filtering the DataFrame to keep only the selected columns")
# Filter the DataFrame to keep only the selected columns
df_selected = df[selected_column_names]

# Print the filtered DataFrame
print(df_selected)

x1= df_selected

print("predicting the output!....")

Y_pred = model.predict(x1)
print(Y_pred)

Y_pred = pd.DataFrame(Y_pred, columns=["Prediction"])



#Output= df3_X.append(Y_pred)
Output= pd.concat([df3_X, Y_pred],axis=1 )

print(type(df_selected))
print(type(Y_pred))

print(df3_X.shape[1])
print(Y_pred.shape[1])

print(Output)
