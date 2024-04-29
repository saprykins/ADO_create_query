# creates queries in different repositories

import requests
import urllib.parse
import base64
from requests.auth import HTTPBasicAuth
import csv


# Azure DevOps organization URL and personal access token (PAT)
personal_access_token = "s***"


# Azure DevOps organization URL and personal access token (PAT)
org_url = "https://dev.a***.com/g***"
YOUR_PROJECT_NAME = 'C***'


# Encode PAT for Basic Authentication
authorization = str(base64.b64encode(bytes(':'+personal_access_token, 'ascii')), 'ascii')

# Read data from CSV file and create queries
with open('POD_all_applications.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # query_name = row['Title'] + ' - ' + row['Entity'] # Assuming 'QueryName' is the column title for query names in the CSV
        query_name = row['Title']

        # Query parameters
        query_path = "Shared Queries/Entities/" + row['Entity']  # Updated query path
        query_count = 0

        # Encode special characters in the query path
        encoded_query_path = urllib.parse.quote(query_path)

        # Azure DevOps API endpoint for creating queries
        api_url = f"{org_url}/{YOUR_PROJECT_NAME}/_apis/wit/queries/{encoded_query_path}?api-version=6.0"

        query_id = row['ID']  # Assuming 'System.Id' is the column title for work item IDs in the CSV
        query_count += 1

        query_body = {
            "name": query_name,
            "wiql": f"SELECT [System.Title], [System.State], [System.AssignedTo], [Custom.Planneddate] \
                FROM workitemLinks \
                WHERE \
                    ( \
                        [Source].[System.TeamProject] = @project \
                        AND [Source].[System.WorkItemType] = 'Epic' \
                        AND [Source].[System.Id] = {query_id} \
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
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + authorization
        }

        # Send POST request to create the query
        response = requests.post(api_url, headers=headers, json=query_body)
        
        # Check if the query was created successfully
        if response.status_code == 201:
            print(f"Query '{query_name}' created successfully.")
        else:
            print(f"Failed to create query '{query_name}'. Status code: {response.status_code}")
            print(response.text)
