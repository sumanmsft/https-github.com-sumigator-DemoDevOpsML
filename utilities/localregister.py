from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core import Run
import argparse

model_name='mobilenet.retrained.soda_cans'

ws = Workspace.from_config()
model = Model.register(ws,model_name = model_name, model_path = "models/"+model_name)

print('Model registered: {} \nModel Description: {} \nModel Version: {}'.format(model.name, model.description, model.version))