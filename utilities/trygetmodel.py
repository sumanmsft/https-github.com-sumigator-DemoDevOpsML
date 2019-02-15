from azureml.core import Workspace
from azureml.core.model import Model

ws = Workspace.from_config()
model_name = "mn.flowers"
Model(ws, model_name).download(model_name)