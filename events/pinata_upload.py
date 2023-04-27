import requests
import json

def create_pinata(EVENT_NAME,IMAGE_PATH,EVENT_DESCRIPTION):
    IMAGE_PATH = str(IMAGE_PATH)
    img_name = IMAGE_PATH.split('/')[0]    
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    files=[
    ('file',(img_name,open(IMAGE_PATH,'rb'),'application/octet-stream'))
    ]

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJjNWM0ODA2OS00ZmVkLTQxMDMtYThiYi0xYWM3MjkxNzU1N2QiLCJlbWFpbCI6ImFzaGlsc2hhaDIwMDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjBkZTkxYTY4ZWJmOTU3NTVhYTIyIiwic2NvcGVkS2V5U2VjcmV0IjoiMTI3ZjdkZTM5MzEwM2E0NGFmYWI3YzYwODllY2IxMzIzODI4OTVlYjM2MDZkYWU3ZWQ1Mjg4OTk0M2RjNTg2MCIsImlhdCI6MTY4MTkyNTY2MX0.8VXKhjRZYgQm8YezoutHF1QI3QkdHbhoFugeR_GBWDs'
    }   

    response = requests.request("POST", url, headers=headers, data={}, files=files)    
    hashcode = json.loads(response.text)["IpfsHash"]   
    print("Image Hash: ",hashcode)

    ## Uplaod JSON

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    payload={
    "attributes": [
        {
            "trait_type": "Event Name",
            "value": EVENT_NAME
        }
    ],
    "description": EVENT_DESCRIPTION,
    "image": "https://ipfs.io/ipfs/"+str(hashcode),
    "name": EVENT_NAME,
     
    }

    headers = {'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJjNWM0ODA2OS00ZmVkLTQxMDMtYThiYi0xYWM3MjkxNzU1N2QiLCJlbWFpbCI6ImFzaGlsc2hhaDIwMDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjBkZTkxYTY4ZWJmOTU3NTVhYTIyIiwic2NvcGVkS2V5U2VjcmV0IjoiMTI3ZjdkZTM5MzEwM2E0NGFmYWI3YzYwODllY2IxMzIzODI4OTVlYjM2MDZkYWU3ZWQ1Mjg4OTk0M2RjNTg2MCIsImlhdCI6MTY4MTkyNTY2MX0.8VXKhjRZYgQm8YezoutHF1QI3QkdHbhoFugeR_GBWDs'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    hashcode = json.loads(response.text)['IpfsHash']
    NFT_URI = "https://ipfs.io/ipfs/"+str(hashcode)
    print(NFT_URI)
    return NFT_URI

if __name__ == '__main__':
    create_pinata('IMage Demo Event','static/images/poster.jpg','this is demo Desc')
