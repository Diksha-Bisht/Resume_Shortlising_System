# Candidate Shortlisting System

It is a small project made using Python to help recruiters get easy insight into candidate's resume quickly and efficiently.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required dependencies.

```bash
pip install pandas PyPDF2 spacy && python -m spacy download en_core_web_sm
```

## Usage

```python
import os 
import pandas as pd     
import PyPDF2           
import spacy    
```

## Directions to Use

Step 1: Download the ``` First.py ``` file. 

Step 2: Install all the dependencies using ``` pip ```.

Step 3: Run the code. 



###  Input

Path of folder where all resumes are stored.

Path of folder where the output file is required to be stored.

### Output

.xlsx (excel) sheet containing all required details.

### Columns in Excel Output
1. Name
2. Summary
3. E-mail Id
4. Contact Number
5. LinkedIn
6. Github
7. Originality

# Constrains
The code works only on ```.pdf``` file format data, and ignores all other kind of file format. Also if the output folder is not found it create one and store the output excel file with name ``` Generated Summary.xlsx ```.

# Use of Packages

1. OS : For interacting with Operating System, file management, and working with directories.
2. Pandas :  For working with data-frames.
3. PyPDF2 : For working with PDF files.
4. SpaCy : For text Processing.





