# ResumeRevealer: Advanced Resume Parsing for MINeD 2024
# Team Unstable Diffusers
### Team Members: Pranshav Patel, Dhruv Thakkar, Kavya Patel, Hetul Shah, Prachita Patel
(🎉We emerged as the winners of this track!)
## Overview
ResumeRevealer is developed for the MINeD 2024 Hackathon, targeting the "PeopleMetrics: Shaping the Next-Gen Workforce" track sponsored by Revelio Labs. This project focuses on the "ResumeRevealer" challenge, aiming to advance resume parsing technology. ResumeRevealer is capable of extracting detailed information from resumes in various formats, classifying text into distinct sections, and sequencing them by dates. It also standardizes job titles against the O-NET database and implements advanced skill extraction.

## Features
- **Comprehensive Resume Parsing**: Handles multiple file formats including PDF, JPG, HTML, DOC, etc., accurately classifying and sequencing resume sections.
- **Job Title Standardization**: Utilizes the O*NET database to ensure consistency in job title taxonomy across resumes.
- **Named Entity Recognition**: Helps in extracting the necessary entities. Designation, Skills and Company name as our entities
- **Advanced Skill Extraction**: Mines detailed skills and competencies from the resume, highlighting specific abilities and expertise. Includes abstractive skill extraction as a bonus feature.

## Installation
1. Clone the repository:
`git clone https://github.com/pranshavpatel/MINeD-hackathon.git`
2. Navigate to the project directory:
`cd MINeD-hackathon`
3. Install the required dependencies:
`pip install -r requirements.txt`


## Usage
To parse a resume and extract detailed information, run:
`python3 resume_parser.py`

## Demonstration
A Jupyter Notebook (`resume_parser.ipynb`) is included to demonstrate the capabilities of ResumeRetreaver. It showcases the parsing, classification, standardization, and skill extraction processes using sample resumes.

## Dataset
An initial dataset of 25-30 resumes across various formats and professions is provided for development and testing. We used a pre-built resume dataset which had `named-entity-recognition` annotations for 200 resumes and used them to fine-tune our `named-entity-recognition` model using spaCy.
Since we couldn't add all the files on github because of it's restructions, we've provided the dataset files and pre-trained models at this [link](https://drive.google.com/drive/folders/1pdWNh0hcv6z_q8MG04dK4InaJHyC5ZFu?usp=sharing).

## Submission Requirements
For the MINeD 2024 Hackathon, submissions must include:
- Python scripts for the tool
- A Python Jupyter notebook for demonstration
- A `requirements.txt` file for dependencies
- This `README.md` file with installation and operation instructions


## Acknowledgements
This project was developed as part of the MINeD 2024 Hackathon, under the guidance of our mentor, Praxal Patel. Special thanks to Revelio Labs for sponsoring the "PeopleMetrics: Shaping the Next-Gen Workforce" track.


