#----------------------------------------------------------------------
# %%time
from google.colab import drive
drive.mount('/content/drive')
#----------------------------------------------------------------------
# machine specifications:
import platform
print(platform.machine())
print(platform.version())
print(platform.platform())
print(platform.uname())
print(platform.system())
print(platform.processor())
#----------------------------------------------------------------------
# %%time
# !pip install spacy
# !python -m spacy download en_core_web_sm
# !pip install PyMuPDF
# !pip install python-docx
# !pip install beautifulsoup4 lxml
# !pip install pytesseract
# !sudo apt-get install tesseract-ocr
# !pip install tensorflow
# !pip install sentence_transformers
# !pip install transformers
#----------------------------------------------------------------------
# %%time
import json
import re
import fitz
from docx import Document
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
#----------------------------------------------------------------------
# %%time
def doc2text(file_path):
    if file_path.endswith('pdf'):
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text

    elif file_path.endswith('docx'):
        document = Document(file_path)
        text = []
        for paragraph in document.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)

    elif file_path.endswith('html'):
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'lxml')
        return soup.get_text(separator='\n', strip=True)

    elif file_path.endswith('jpg') or file_path.endswith('jpeg') or file_path.endswith('png'):
      image = Image.open(file_path)
      extracted_text = pytesseract.image_to_string(image)
      return extracted_text
#----------------------------------------------------------------------
# %%time
sec = [[#skills
        'areas of experience',
        'areas of expertise',
        'areas of knowledge',
        'skills',

        "other skills",
        "other abilities",
        'career related skills',
        'professional skills',
        'specialized skills',
        'technical skills',
        'soft skills',
        'computer skills',
        'personal skills',
        # 'computer knowledge',
        # 'technologies',

        'proficiencies',
        'languages',
        'language competencies and skills',
        'programming languages',
        'competencies'
],
      [#experience
        'employment history',
        'employment data',
        'career summary',
        'work history',
       'technical experience',
        'working history',
        'work experience',
        'experience',
        'professional experience',
        'professional background',
        'professional employment',
        'additional experience',
        'career related experience',
        "professional employment history",
        'related experience',
        'relevant experience',
        'programming experience',
        'freelance',
        'freelance experience',
        'internship experience',
        'internships',
        'apprenticeships',
        'army experience',
        'military experience',
        'military background',
               'special training',
       'training'

],
[#education
        'academic background',
        'academic experience',

        'courses',
        'qualification',
        'related courses',
        'education',
        'educational background',
        'educational qualifications',
        'educational training',
        'education and training',
        'academic training',
        'Academic Qualification',
        #'professional training',
        'course project experience',
        'related course projects',
        'college activities',
        'certifications',
    ],



[#miscellaneous
        'activities and honors',
        #'activities',
        'affiliations',
        'professional affiliations',
        'associations',
        'professional associations',
        'memberships',
        'professional memberships',
        'athletic involvement',
        'community involvement',

        'civic activities',
        'extra-Curricular activities',
        'professional activities',
        'volunteer work',
        'volunteer experience',
        'additional information',

],

[#achievements
        'achievement',
        'achievements',
        'awards and achievements',
        'licenses',
        'license',

        'conference presentations',
        'conventions',
        'dissertations',
        'exhibits',
        'papers',
        'publications',
        'professional publications',
        'research experience',
        'research grants',


        'research projects',
        'personal projects',
        'current research interests',

]
]

section_names=["skills","experience","education","miscellaneous","achievements"]
check_segmented = [
    False,
    False,
    False,
    False,
    False,

]

def classify_sections(text):
    # custom logic for classifying sections (similar to the previous example)
    sections = {}
    current_section = None
    temp=False
    for line in text.split('\n'):
     # print(line)
      temp=False
      for section_keywords in sec:
        if  (check_segmented[sec.index(section_keywords)]==False) and any((keyword.lower() in line.lower())  for keyword in section_keywords):
            for i in range(len(check_segmented)):
              check_segmented[i]=False
            check_segmented[sec.index(section_keywords)] = True

            temp=True
            current_section =section_names[sec.index(section_keywords)]
            if sections.get(current_section,0)!=0:
              continue
            sections[current_section] = []
            break
      if current_section !=None and temp==False:
        sections[current_section].append(line)


    return sections

def parse_resume(path):
    text = doc2text(path)
    sections = classify_sections(text)
    return text, sections

#----------------------------------------------------------------------
# %%time
import pandas as pd
df=pd.DataFrame(columns=section_names)
df
#----------------------------------------------------------------------
# %%time
import os
resume_content=''
for filename in os.listdir("hackathon/resume-data"):

    resume_content, sections = parse_resume('hackathon/resume-data/Charles Obuseh.pdf')
    df=df.append(sections,ignore_index=True)
    print("Resume Sections:")
    for section, content in sections.items():
      print(section.capitalize() + "   :")

      print('\n'.join(content))

      print("-----------------")
    break
    print("******************************************************************")
#----------------------------------------------------------------------
# %%time
# Define a function to concatenate skill and experience for each row
def concatenate_skills_experience(row):
    # Convert the list of skills to a string
    skills_str = ', '.join(row['skills']) if isinstance(row['skills'], list) else str(row['skills'])
    # Convert the element in the 'experience' column to a string
    experience_str = ', '.join(row['experience']) if isinstance(row['experience'], list) else str(row['experience'])
    return skills_str + ', ' + experience_str

# Create a new DataFrame 'x' with the 'skills' and 'experience' columns
x = df[['skills', 'experience']].copy()

# Apply the concatenate_skills_experience function to each row and assign the result to column 'y'
x['y'] = x.apply(concatenate_skills_experience, axis=1)

# Drop the original 'skills' and 'experience' columns
x.drop(['skills', 'experience'], axis=1, inplace=True)

x

#----------------------------------------------------------------------
# %%time
import spacy
import pandas as pd

# Load the English language model in SpaCy
nlp = spacy.load("en_core_web_sm")

# Function to extract noun phrases from text using SpaCy
def extract_noun_phrases(text):
    doc = nlp(text)
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    return noun_phrases

# Load the DataFrame 'x' created in the previous code
# Replace 'x.csv' with the actual file path if saving/loading from a file


# Extract noun phrases from the 'y' column of DataFrame 'x'
noun_phrases = []
for text in x['y']:
    noun_phrases.extend(extract_noun_phrases(text))

noun_phrases
#----------------------------------------------------------------------
# %%time
import pandas as pd
df1 = pd.read_csv(r'hackathon/noun_phrases_1.csv')
df2 = pd.read_csv(r'hackathon/noun_phrases_2.csv')


# Append df2 to df1
merged_df = df1.append(df2)
merged_df
#----------------------------------------------------------------------
# %%time
merged_df = merged_df.sample(frac=1, random_state=42)
merged_df.reset_index(drop=True, inplace=True)
#----------------------------------------------------------------------
# %%time
merged_df['noun_phrase']
#----------------------------------------------------------------------
# %%time
mapping = {'skills': 1, 'non_skills': 0}

merged_df[' skills/non_skills'] = merged_df[' skills/non_skills'].map(mapping)

#----------------------------------------------------------------------
# %%time
merged_df
#----------------------------------------------------------------------
# %%time
merged_df['noun_phrase'] = merged_df['noun_phrase'].astype(str)
#----------------------------------------------------------------------
# %%time
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import SpatialDropout1D, LSTM, Conv1D, GlobalMaxPooling1D, Dense, Embedding
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
# Tokenize the noun phrases
tokenizer = Tokenizer()
tokenizer.fit_on_texts(merged_df['noun_phrase'])
X_sequences = tokenizer.texts_to_sequences(merged_df['noun_phrase'])
print(X_sequences)
# Pad sequences to ensure uniform length
max_length = 100
X_padded = pad_sequences(X_sequences, maxlen=max_length, padding='post')

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_padded, merged_df[' skills/non_skills'], test_size=0.2, random_state=42)

# Define the model
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=100, input_length=max_length),
    Conv1D(filters=128, kernel_size=5, activation='relu'),
    GlobalMaxPooling1D(),
    # Flatten(),
    Dense(units=10, activation='relu'),
    Dense(units=1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print model summary
print(model.summary())

# Train the model
model.fit(X_train, y_train, epochs=30, batch_size=32)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

#----------------------------------------------------------------------
# %%time
model.save('hackathon/model.h5')
#----------------------------------------------------------------------
# %%time
text='\n'.join(df['skills'][0])
# text+=df['experience'][0]
text+='\n'.join(df['experience'][0])
text
#----------------------------------------------------------------------
# %%time
def extract_skills(text):
    noun_phrases = extract_noun_phrases(text)
    noun_phrases = np.array(noun_phrases).astype(str)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(noun_phrases)
    X_sequences = tokenizer.texts_to_sequences(noun_phrases)

    # Pad sequences to ensure uniform length
    max_length = 100
    X_padded = pad_sequences(X_sequences, maxlen=max_length, padding='post')

    # Reshape input data to add embedding dimension
    X_padded = np.expand_dims(X_padded, axis=-1)  # Add embedding dimension

    predictions = model.predict(X_padded)

    # Filter predicted skills based on the threshold
    threshold = 0.5  # Adjust as needed
    predicted_skills = [noun_phrases[i] for i, pred in enumerate(predictions) if pred > threshold]

    return predicted_skills

#----------------------------------------------------------------------
# %%time
extracted_skills = extract_skills(text)
#----------------------------------------------------------------------
# %%time
print(f'Extracted Skills: {extracted_skills}')
#----------------------------------------------------------------------
# %%time
final_skills = '\n'.join(extracted_skills)
#----------------------------------------------------------------------
# %%time
nlp_model = spacy.load('hackathon/skills_model')
# text=df['skills']
doc = nlp_model(final_skills)
abstractive_skills=''
for ent in doc.ents:
  abstractive_skills+=ent.text
  print(f'{ent.label_.upper()}->\n {ent.text}')
#----------------------------------------------------------------------
df
#----------------------------------------------------------------------
# %%time
final_designation = '\n'.join(df['experience'][0])
final_designation
#----------------------------------------------------------------------
# %%time
store_designations = []

nlp_model_d = spacy.load('hackathon/designation_model')
doc = nlp_model_d(final_designation)
for ent in doc.ents:
    store_designations.append(ent.text)
    print(f'{ent.label_.upper():{30}}- {ent.text}')
#----------------------------------------------------------------------
# %%time
store_designations
#----------------------------------------------------------------------
# %%time
# Get the file path
file_path = 'hackathon/data.csv'

# Read the CSV file into a DataFrame
df_ = pd.read_csv(file_path)

# Get the desired column as a list
labels = df_['Title'].tolist()
codes = df_['O*NET Code'].tolist()
res = dict(zip(labels, codes))
#----------------------------------------------------------------------
# %%time
model2 = SentenceTransformer('all-MiniLM-L6-v2')
#----------------------------------------------------------------------
# %%time
standard_job_titles = labels
standard_embeddings = model2.encode(standard_job_titles)
#----------------------------------------------------------------------
# %%time
extracted_job_titles = store_designations
extracted_embeddings = model2.encode(extracted_job_titles)
#----------------------------------------------------------------------
# %%time
# Function to find the most similar standard job title for each extracted job title
def find_most_similar_jobs(extracted_embeddings, standard_embeddings, standard_job_titles):
    for extracted_embedding in extracted_embeddings:
        similarities = util.cos_sim(extracted_embedding, standard_embeddings)
        max_index = np.argmax(similarities)

        yield standard_job_titles[max_index]
#----------------------------------------------------------------------
# %%time
# Mapping each extracted job title to the most similar standard job title
mapped_job_titles = list(find_most_similar_jobs(extracted_embeddings, standard_embeddings, standard_job_titles))
for extracted, mapped in zip(store_designations, mapped_job_titles):
    print(f'Extracted: {extracted} -> Mapped: {mapped}')
#----------------------------------------------------------------------
# %%time
final_education = '\n'.join(df['education'][0])
final_education
#----------------------------------------------------------------------

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# %%time
s=df['experience'][0]
s=' '.join(s)
l=[0]
for i in store_designations:
  l+=[s.index(i)]
l+=[len(s)]
l
se=[]
for i in range(1,len(l)-1):
  se+=[s[l[i]:l[i+1]]]
sk=[]
for d in se:
  sk+=[extract_skills(d)]
sk
#----------------------------------------------------------------------
# %%time
skill_preds=[]
for skill in sk:
  temp='\n'.join(skill)
  doc=nlp_model(temp)
  temp_skills=''
  for ent in doc.ents:
   temp_skills+=ent.text
  skill_preds.append(temp_skills)
#----------------------------------------------------------------------
df
#----------------------------------------------------------------------
# %%time
raw_exp='\n'.join(df.iloc[0]['experience'])
raw_exp
#----------------------------------------------------------------------
# %%time
def replace_strings(work_experience, original_strings, replacement_strings):
    """
    Replace occurrences of strings in 'original_strings' with corresponding strings in 'replacement_strings' in the 'work_experience' text.

    Parameters:
    - work_experience (str): The text containing the work experience.
    - original_strings (list of str): Strings to be replaced.
    - replacement_strings (list of str): Strings to replace with.

    Returns:
    - str: Updated work experience text.
    """
    for original, replacement in zip(original_strings, replacement_strings):
        work_experience = work_experience.replace(original, replacement)
    return work_experience
#----------------------------------------------------------------------
# %%time
final_exp = replace_strings(raw_exp, store_designations, mapped_job_titles)
#----------------------------------------------------------------------
# %%time
for designation, standard_designation in store_designations, mapped_job_titles:
  if designation in raw_exp:
    raw_exp.replace(designation, standard_designation)
#----------------------------------------------------------------------
# %%time
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#----------------------------------------------------------------------
# %%time
import re

def time_line():
  date_pattern = r'\b(?:\d{2}/\d{4}|\d{2}/\d{2}|\d{2}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4})\b'


  #for designation
  date_with_designation = []
  for designations in store_designations:
    index = final_designation.index(designations)
    temp_str = final_designation[index : ]

    dates = re.findall(date_pattern, temp_str)
    if(len(dates) > 0):
      date_with_designation.append(dates[0])





  return date_with_designation

des_date = time_line()

from dateutil.parser import parse

# print(mapped_titles)
# print(des_date)


time = dict(zip(des_date, store_designations))
dates = [parse(date_str) for date_str in des_date]
sorted_dates_with_titles = sorted(zip(dates, store_designations))
sorted_dates = [date.strftime('%Y-%m-%d') for date, _ in sorted_dates_with_titles]
sorted_titles = [title for _, title in sorted_dates_with_titles]
sorted_time = dict(zip(sorted_dates, sorted_titles))

# print(sorted_time)
#----------------------------------------------------------------------
# %%time
print('----------------------------')
print('RESUME DETAILS')
print('----------------------------')
print('----------------------------')
print('EDUCATION')
print('----------------------------')
print('\n'.join(df.iloc[0]['education']))
print('----------------------------')
print('----------------------------')
print('EXPERIENCE')
print('----------------------------')
print('DESIGNATIONS AS PER O*NET DATABASE:')
print('----------------------------')
# print('\n'.join(mapped_job_titles))
for jtitle, desc, skill_pred in zip(mapped_job_titles,se,skill_preds):
  print('***TITLE***')
  print(f'{jtitle} --> {res[jtitle]}')
  print('***DESCRIPTION***')
  print(desc)
  print('***PREDICTED SKILLS***')
  print(skill_pred)
  print('\n')

print('----------------------------')
# print('\n'.join(df.iloc[0]['experience']))
# print(final_exp.strip())
print('----------------------------')
print('ABSTRACTIVE SKILLS')
print('----------------------------')
print(abstractive_skills)
print('----------------------------')
print('----------------------------')
print('SKILLS')
print('----------------------------')
print('\n'.join(df.iloc[0]['skills']))
print('----------------------------')
print('----------------------------')
print('ACHIEVEMENTS')
print('----------------------------')
print('\n'.join(df.iloc[0]['achievements']))
print('----------------------------')
print('----------------------------')
print('CAREER TRAJECTORY')
print('----------------------------')
for key in sorted_time:
  print(f'{key}--->{sorted_time[key]}')
print('----------------------------')
print('----------------------------')


#----------------------------------------------------------------------

