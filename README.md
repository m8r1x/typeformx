# TypeformX
A simple python script to extract typeform data from the typeform api.

### Prerequisites
The following python packages are required to successfully execute the script:
- pandas
- requests
- textblob
- textract

### Basic Usage
```python
from typeformx import TypeformX

api_key = "MY_API_KEY"
# two arguments may be passed to the constructor
#   1. api key issued by typeform
#   2. optional argument boolean 'complete'
#       if true append 'complete=true' at the end of the url to fetch only completed forms the opposite is true.
typeform = TypeformX(api_key, True) 

typeform.get_all_forms() # fetch all typeforms you own
typeform.get_form_answers('TYPEFORM_ID') # fetch all answers from a typeform
typeform.get_form_fields('TYPEFORM_ID') # fetch all fields from a typeform
typeform.get_form_emails('TYPEFORM_ID') #fetch all emails from a typeform
typeform.get_file_upload_urls('TYPEFORM_ID') #fetch all file upload urls from a typeform

```
### Write results to csv file
```python
from typeformx import TypeformX, write_to_csv

api_key = "MY_API_KEY"

typeform = TypeformX(api_key, True)
# all forms
all_forms = typeform.get_all_forms()

for i in range(len(all_forms)):
    extracted_info = typeform.get_email_file_text(form['id'][i])
    filename = form['name'][i].replace(' ', '').replace('/', '').replace('\'', '') # this can be done using a 'clean_filename' function
    for extracted in extracted_info:
        write_to_csv(extracted, filename+'.csv')

```
### Running tests
The tests use the `nosetest` and `mock` packages.<br/>
Open `typeform_test.py` and add your typeform API KEY then<br/>
To run the test script:
`nosetests --verbosity=2`

### API Reference
##### `TypeformX(API_KEY, complete=FALSE)`
* Constructor that takes in two arguments:
    * API_KEY (Compulsory type: `string`)
    * Complete (Optional type: `boolean`)
    
##### `write_to_csv([arr], FILENAME)`
* Method that writes data to a `.csv` file.
    * Takes two arguments :
        * A **list/array** of data to write
        * `String` argument denoting the **filename**
        
#### Instance methods
##### `get_all_forms(TYPEFORM_ID)`
* Method that retrieves all the typeforms owned by a user.
    * Takes one `String` argument : `TYPEFORM_ID`
    * returns a pandas data frame with columns typeform `id` and typeform `name` 
##### `get_form_answers(TYPEFORM_ID)`
* Method that retrieves all answers from a particular typeform.
    * Takes one `String` argument : `TYPEFORM_ID`
    * returns a multidimensional(**2D**) array/list of `strings`
##### `get_form_fields(TYPEFORM_ID)`
* Method that retrieves all question fields from a particular typeform.
    * Takes one `String` argument : `TYPEFORM_ID`
    * returns an array/list of fields.
##### `get_form_emails(TYPEFORM_ID)`
* Method that retrieves all emails from a particular typeform.
    * Takes one `String` argument : `TYPEFORM_ID`
    * returns an array/list of fields
##### `get_email_file_text(TYPEFORM_ID)`
* Method that retrieves all emails, file upload urls and file text from a particular typeform.
    * Takes one `String` argument : `TYPEFORM_ID`
    * returns a multidimensional(**2D**) array/list of `strings`
