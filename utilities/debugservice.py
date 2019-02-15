from azureml.core import Workspace

ws = Workspace.from_config()
with open('debug.log','w') as f:
    f.write(ws.webservices['flowers-devtest'].get_logs())