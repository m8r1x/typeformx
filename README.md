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
from typeformx import TypeformX, write_to_csv

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
### Running tests
The tests use the `nosetest` and `mock` packages.
To run the test script:
`nosetests`

### API Reference
##### `TypeformX(API_KEY, complete=FALSE)`
* Constructor that takes in two arguments:
    * API_KEY (Compulsory type: `string`)
    * Complete (Optional type: `boolean`)
##### `get_all_forms(TYPEFORM_ID)`
* Method that retrieves all the typeforms owned by a user.
    * Takes one `String` argument : `TYPEFORM_ID`
    * returns a multidimensional(**2D**) array/list of `strings`
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
##### `write_to_csv([arr], FILENAME)`
* Method that writes data to a `.csv` file.
    * Takes two arguments :
        * A **list/array** of data to write
        * `String` argument denoting the **filename**