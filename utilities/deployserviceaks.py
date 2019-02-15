from azureml.core import Workspace
from azureml.core.webservice import Webservice,AksWebservice
from azureml.core.compute import AksCompute, ComputeTarget

from azureml.core.model import Model
from azureml.core.image import Image, ContainerImage
import os
import json

ws = Workspace.from_config()

model_name = 'mn.flowers'
model = Model(ws,model_name)

# generate model.json and read this to get the model name
with open('model.json','w') as f:
    f.write(json.dumps({'model_name':model.name}))

image_config = ContainerImage.image_configuration(runtime= "python",
                                 execution_script="score.py",
                                 conda_file="infenv.yml",
                                 dependencies=["model.json"]
                                 )


aksconfig = AksWebservice.deploy_configuration(cpu_cores = 1, 
                                               memory_gb = 1)

service_name = model_name.replace('.','-').replace('_','-') + '-prod'
print(service_name)

akscluster = ComputeTarget(ws,name='aks012405')

image = ContainerImage.create(ws,models=[model],image_config = image_config,name=model_name)
image.wait_for_creation(show_output = True)

service = AksWebservice.deploy_from_image(workspace = ws,
                                            deployment_config = aksconfig,
                                            deployment_target = akscluster,
                                            name = service_name,
                                            image = image)

service.wait_for_deployment(True)
print(service.state)