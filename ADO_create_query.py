import requests
import urllib.parse
import base64
from requests.auth import HTTPBasicAuth


# Azure DevOps organization URL and personal access token (PAT)
personal_access_token = "m*"


# Azure DevOps organization URL and personal access token (PAT)
org_url = "https://dev.azure.com/g*"
YOUR_PROJECT_NAME = 'POD_Factory_v5'

# Query parameters
query_path = "Shared Queries/Tst"  # Updated query path
query_name_prefix = "template_14"
query_count = 1

# Encode special characters in the query path
encoded_query_path = urllib.parse.quote(query_path)

# Azure DevOps API endpoint for creating queries
api_url = f"{org_url}/{YOUR_PROJECT_NAME}/_apis/wit/queries/{encoded_query_path}?api-version=6.0"

# Personal Access Token (PAT)
# personal_access_token = "YOUR_PERSONAL_ACCESS_TOKEN"

# Encode PAT for Basic Authentication
authorization = str(base64.b64encode(bytes(':'+personal_access_token, 'ascii')), 'ascii')

# HTTP headers and query body
headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + authorization
}

# Create 100 queries
for i in range(1, query_count + 1):
    query_name = f"{query_name_prefix} {i}"
    query_body = {
        "name": query_name,
        
        "wiql": "SELECT \
            [System.Id], \
            [System.WorkItemType], \
            [System.Title], \
            [System.AssignedTo], \
            [System.State], \
            [System.Tags] \
        FROM workitemLinks \
        WHERE \
            ( \
                [Source].[System.TeamProject] = @project \
                AND [Source].[System.WorkItemType] = 'User Story' \
                AND [Source].[System.Id] = 333055 \
            ) \
            AND ( \
                [System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward' \
            ) \
            AND ( \
                [Target].[System.TeamProject] = @project \
                AND [Target].[System.WorkItemType] <> '' \
            ) \
        MODE (Recursive)",

        "isFolder": False,
        "queryType": "tree",
        "isRecursive": True
    }
    
    # Send POST request to create the query
    response = requests.post(api_url, headers=headers, json=query_body)
    
    # Check if the query was created successfully
    if response.status_code == 200:
        print(f"Query '{query_name}' created successfully.")
    else:
        print(f"Failed to create query '{query_name}'. Status code: {response.status_code}")
        # print(response.text)
