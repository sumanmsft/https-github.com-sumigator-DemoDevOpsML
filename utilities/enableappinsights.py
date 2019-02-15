from azureml.core import Workspace
from azureml.core.webservice import Webservice

ws = Workspace.from_config()

for endpoint in ws.webservices:
    print(endpoint)
    Webservice(ws,endpoint).update(enable_app_insights=True)