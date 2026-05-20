from pageindex import PageIndexClient
from dotenv import load_dotenv
load_dotenv()
import os

#init client
pi_client = PageIndexClient(api_key=os.getenv("PAGE_INDEX_API_KEY"))

#add document
result = pi_client.submit_document("ml.pdf")
#get doc id
doc_id = result["doc_id"]

#check status
status = pi_client.get_document(doc_id)["status"]
if status == "completed":
    print('Document processing completed')

print(f"Document ID: {doc_id}")

#doc id = pi-cmpe2c2vj021701pnfxokeohi