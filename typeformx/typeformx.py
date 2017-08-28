import csv
import json
import pandas as pd
import re
import requests
from textblob import TextBlob
from textract import process

def get_form(api_key, typeform_id, complete=False):
    typeform_base_url = 'https://api.typeform.com/v1/form/'
    # append the api key at the end of the url
    base_url = typeform_base_url +typeform_id + '?key=' +api_key
    
    # check for the complete option and add it to the url 
    # to get completed results only
    if complete:
        base_url += '&completed=true'

    # return a json object / python dict
    return requests.get(base_url).json()
    
def get_typeform_answers(api_key, typeform_id, complete):
    # get the response field from the json results
    typeform_responses = get_form(api_key, typeform_id, complete)['responses']
    # extract answers field from each response
    typeform_answers = [response['answers'] for response in typeform_responses]
        
    return typeform_answers
        
def write_to_csv(arr, csv_filename):
    try:
        with open(csv_filename, 'ab') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(arr)
    except IOError:
        print("Error! Could not write to file!")
        
def download_file(url):
    file_extensions = ['csv', 'doc', 'docx', 'eml', 'epub', 'gif', 'htm', 'html', 'jpeg', 'jpg', 'json', 'log', 'mp3', 'msg', 'odt', 'ogg', 'pdf', 'png', 'pptx', 'ps', 'psv', 'rtf', 'tff', 'tif', 'tiff', 'tsv', 'txt', 'wav', 'xls', 'xlsx']
    if url is not None:
        filename = url.split('/')[-1] # extract final part of url
        filename = filename.split('?')[0] # remove query parameters
        extension = filename.split('.')[-1] # extract extension
        
        if extension not in file_extensions:
            return None
            
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        try:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
        except IOError:
            print("Error! Download failed! Could not write to file!")
            
        return filename
        
    return None

def extract_text(filename):
    if filename is not None:
        return process(filename)
        
    return None

def extract_file_text(url):
    file = download_file(url)
    try:
        extracted_text = extract_text(file).decode('unicode-escape').encode('ascii', 'ignore')
    except UnicodeDecodeError:
        print("Error while decoding text...")

    # convert textblob's sentence SET list 
    #       [Sentence('...'), Sentence('...'), ...]
    # to normal python list
    sentences = [''.join(list(sentence)) for sentence in TextBlob(extracted_text).sentences]
    return ' '.join(sentences)
    
class TypeformX:
    def __init__(self, api_key, complete=False):
        self.api_key = api_key
        self.complete = complete
        
    def get_all_forms(self):
        base_url = 'https://api.typeform.com/v1/forms?key='
        base_url += self.api_key
        
        api_response = requests.get(base_url).json()
        cols = ['id', 'name']
        api_response_length = len(api_response)
        
        typeform_frame = pd.DataFrame(columns=cols, index=range(api_response_length))
        
        for i in range(api_response_length):
            typeform_frame.id[i] = api_response[i]['id']
            typeform_frame.name[i] = api_response[i]['name']
            
        return typeform_frame
        
    def get_form_answers(self, typeform_id):
        return get_typeform_answers(self.api_key, typeform_id, self.complete)
        
    def get_form_fields(self, typeform_id):
        # get the questions field from json response
        typeform_questions = get_form(self.api_key, typeform_id)['questions']
        typeform_fields = set() # to capture each field only once
        
        # check for multiple choice fields and tag them
        for question in typeform_questions:
            if question['id'].lower().startswith('list'):
                question['question'] += '_multiple_choice'
            
            typeform_fields.add(question['question'])
            
        return list(typeform_fields)
        
    def get_form_emails(self, typeform_id):
        emails = []
        for answers in get_typeform_answers(self.api_key, typeform_id, self.complete):
            for answer in answers.values():
                x = re.search('\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', answer)
                if x:
                    emails.append(x.group())
                    
        return emails
        
    def get_file_upload_urls(self, typeform_id):
        file_upload_links = []
        answers = get_typeform_answers(self.api_key, typeform_id, self.complete)
        
        for answer in answers:
            for key in answer.keys():
                if key.startswith('fileupload'):
                    file_upload_links.append(answer[key])
                    
        return file_upload_links

    def get_email_file_text(self, typeform_id):
        extracted_data = []
        
        for obj in get_typeform_answers(self.api_key, typeform_id, self.complete):
            for key in obj.keys():
                x = re.search('\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', obj[key])
                if x:
                    email = x.group()
                    
                if key.startswith('fileupload'):
                    cv_link = obj[key]
                
            try:
                extracted_text = extract_file_text(cv_link)
                extracted_data.append([email, cv_link, extracted_text])
            except AttributeError: # caused when text extraction function returns 'None'
                print("No file upload url found... Encountered NoneType")
            except UnboundLocalError: # caused when typeform has no upload file fields
                print("No fileupload field found")
                
                
        return extracted_data
        
def main():
    api_key = input('Enter API_KEY: ')
    typeform = TypeformX(api_key)
    typeform_df = typeform.get_all_forms()
    print('\n')
    print(typeform_df)
    
    operation = int(input('\nEnter Operation\n0. Exit\n1. Get Form Fields\n2. Get Form Answers\n\nOperation: '))
    if operation == 0:
        exit()
    
    form_id = int(input('\nEnter typeform id number from above list: '))
    
    if operation == 1:
        fields = typeform.get_form_fields(typeform_df['id'][form_id])
        print('\n')
        print(fields)
    elif operation == 2:
        answers = typeform.get_form_answers(typeform_df['id'][form_id])
        print('\n')
        print(answers)

if __name__ == '__main__':
    main()
