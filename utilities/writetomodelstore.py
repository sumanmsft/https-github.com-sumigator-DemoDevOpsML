from vsts.vss_connection import VssConnection
from msrest.authentication import BasicAuthentication
import pprint
import json
from vsts import git

# Fill in with your personal access token and org URL
with open('keys.json', 'r') as f:
    keys = json.load(f)
personal_access_token = keys['devopsPat']
print(personal_access_token)
organization_url = keys['devopsAccount']
repository_id = keys['modelGalleryRepoId']
# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = VssConnection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
client = connection.get_client('vsts.git.v4_1.git_client.GitClient')

from azureml.core import Workspace
from azureml.core.model import Model

ws = Workspace.from_config()
for m in ws.models:
    model = Model(ws,m)
    odelInfo = 'Model registered: {} \nModel Description: {} \nModel Version: {}'.format(model.name, model.description, model.version)
    
    latestCommit = client.get_branch(repository_id,'master').commit.commit_id

    push = {
    "refUpdates": [
        {
        "name": "refs/heads/master",
        "oldObjectId": latestCommit
        }
    ],
    "commits": [
        {
        "comment": "Added task markdown file.",
        "changes": [
            {
            "changeType": "add",
            "item": {
                "path": '{}/{}/{}/metadata.yml'.format(ws.name,model.name,model.version)
            },
            "newContent": {
                "content": "model-metadata",
                "contentType": "rawtext"
            }
            }
        ]
        }
    ]
    }

    client.create_push(push, repository_id)

print('all done!')