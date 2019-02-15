from azureml.core import Workspace
from azureml.core.webservice import Webservice,AciWebservice
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

aciconfig = AciWebservice.deploy_configuration(cpu_cores = 1, 
                                               memory_gb = 1,
                                               enable_app_insights=True)

aci_service_name = model_name.replace('.','-').replace('_','-') + '-test'
print(aci_service_name)

image = ContainerImage.create(ws,models=[model],image_config = image_config,name=model_name)
image.wait_for_creation(show_output = True)

aci_service = Webservice.deploy_from_image(workspace = ws,
                                            deployment_config = aciconfig,
                                            name = aci_service_name,
                                            image = image)

aci_service.wait_for_deployment(True)
print(aci_service.state)