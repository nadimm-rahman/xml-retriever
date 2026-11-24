# xml-retriever
Retrieving XML objects for ENA database tables using Python.

## Usage

This script often is used to obtain a bunch of XMLs in order to update objects in bulk later. Although it is currently geared towards runs/experiments, it is technically usable for a wider range of data objects, as the code itself is generic enough.

1. Clone the repository.
2. Edit retrieve.py to include appropriate database connections, list of accessions to retrieve and the SQL query.
3. The list of accessions are used by the SQL query to get the XML objects, so ensure you have the correct SQL query based on the list of accessions.
4. Check the name of the output XML towards the top of the script. You can choose to add a directory name ahead of the name of the file.
5. Run the python script.

## Output

You will receive one XML of all the XML objects searched for via the SQL query.

This can be edited as appropriate in preparation for programmatic updates that can be done in bulk. An example command is listed below:

```
curl --fail-with-body -sS \
  -u "$ENA_USER:$ENA_PASSWORD" \
  -F "SUBMISSION=@submission.xml" \
  -F "EXPERIMENT=@experiment_set.xml" \
  "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/" \
  -o ena_receipt.xml
```

Here, the output is captured in a receipt file. Remember to create a submission XML file as per ENA's documentation for updating data.
