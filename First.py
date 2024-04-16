
# --------- Resume Shortlisting System ---------------

#Importing Libraries

import os    # For interacting with Operating System
import pandas as pd     # For working with dataframes
import PyPDF2           # For working with PDF files
import spacy            # For text Processing

# Uploading and Validating Resume Folder and its Content

def validateAndList(folderPath):

    # Validating resume folder path
    if not os.path.isdir(folderPath):
        print("\n!!! Path not found !!!")
        return

    print("\nFolder uploaded successfully \n")

    # Validating content of folder (Folder should contain resume in pdf format only)
    pdfFiles = []        # To store names of .pdf files seperately for future reference
    fileCount = 0        # To keep count of total files inside a folder

    for file in os.listdir(folderPath):
        filePath = os.path.join(folderPath, file)
        # Checking if file exist or not
        if os.path.isfile(filePath):
            fileCount +=1
            # Checking if file is pdf or not
            if file.lower().endswith('.pdf'):
                pdfFiles.append(file)
            else:
                print(f"{file} is not in .pdf file format hence can not process this. \n")

    print(f"Total number of valid files found are: {len(pdfFiles)} out of {fileCount}")
    return pdfFiles

# Getting Linked Profile of the Candidate
def extractLinkedin(text):
    linkedin= r'LinkedIn[\s:]+(.*?)(?=(?:\n[A-Z]|$))'
    matchlinkedin = re.search(linkedin, text, re.IGNORECASE)
    if matchlinkedin:
        return matchlinkedin.group(1).strip()
    return ""

# Getting GitHub Profile of the Candidate
def extractGithub(text):
    github = r'GitHub[\s:]+(.*?)(?=(?:\n[A-Z]|$))'
    matchgithub = re.search(github, text, re.IGNORECASE)
    if matchgithub:
        return matchgithub.group(1).strip(' ')
    return ""

# Getting Summary about Profile of the Candidate
def extractSummary(text):
    nlp = spacy.load("en_core_web_sm")
    d = nlp(text)
    sentence = [s.text for s in d.sents]
    summary = " ".join(sentence[:2])
    return summary

# Getting Email Id and Contact Number of the Candidate
def extractEmailPhno(text):
    # Extracting Email Id
    email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

    # Extracting Contact Number
    phno = re.findall(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b', text)
    formatphno = [''.join(num) for num in phno]      #Removing unwanted elements

    return email, formatphno


# Getting Information about Profile of the Candidate
def extractText(filePath):
    with open(filePath, "rb") as fi:
        reader = PyPDF2.PdfReader(fi)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text.lower()


def process_data(folder, files):
    result = []

    for file in files:
        filePath = os.path.join(folder, file)
        try:
            # Extracting details
            text = extractText(filePath)
            email, phno = extractEmailPhno(text)
            summary = extractSummary(text)
            linkedin = extractLinkedin(text)
            github = extractGithub(text)

            result.append({ 'Name' : os.path.splitext(file)[0],
                           'Summary' : summary,
                           'E-mail Id' : email,
                           'Contact Number' : phno,
                           'LinkedIn' : linkedin,
                           'Github' : github })
        # Exception Handeling
        except Exception as ex:
            print(f" !! ERROR !! : {file} : {ex}")
            continue

    return pd.DataFrame(result)


if __name__ == "__main__":
    inpFolderPath= input("Enter the path of folder containing all the resumes \n(NOTE: The content inside subfolders will not be considered): ")

    validFiles = validateAndList(inpFolderPath)     #Validation function to validate folder path and content of the folder

    # Collecting all necessary details like name, summary, email, contact number, githu, and linkedin
    print("\n\nPROCESSING....")
    df = process_data(inpFolderPath,validFiles)

    # Displaying Output
    response = input('Do you want to download the final report in excel file format? \nEnter Y for Yes. ')

    if response.lower() == 'y':
        outputFolder = input("Enter the path for output folder: ")
        if not os.path.exists(outputFolder):
            os.mkdirs(outputFolder)
        outputFile = os.path.join(outputFolder, 'Generated Summary.xlsx' )
        print("\n............ File Saved Successfully ..................")

        df.to_excel(outputFile, index = False)
    else:
        print(f"Final output is:\n {df}")



