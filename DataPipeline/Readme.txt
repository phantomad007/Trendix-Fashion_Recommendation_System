To install all the dependent libraries save the text file with below lines and save as requirements.txt in same the folder as coding file

now run "pip install -r requirements.txt"


To connect storage from driver in local directory to a bucket in cloud storage:

> Create a bucket in cloud storage, and change the bucket name in code.

> Create a Service Account and download JSON credential file

1. Enable Cloud Storage API 
>>API&Services>>library>>enable cloud storage API

2. Create a Service account in IAM&Admin 

3. Grant permission to the service account, give a role(owner: Storage admin and add others as per)

4. Create a new key in create&manage keys and download the JSON file available the (3 dot)menu 

Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "PATH of JSON FILE"


