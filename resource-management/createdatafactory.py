import os
import azureml.core
from azureml.core.compute import ComputeTarget, DataFactoryCompute
from azureml.exceptions import ComputeTargetException
from azureml.core import Workspace, Experiment
from azureml.pipeline.core import Pipeline
from azureml.core.datastore import Datastore
from azureml.data.data_reference import DataReference
from azureml.pipeline.steps import DataTransferStep

ws = Workspace.from_config()

data_factory_name = 'adf'

def get_or_create_data_factory(workspace, factory_name):
    try:
        return DataFactoryCompute(workspace, factory_name)
    except ComputeTargetException as e:
        if 'ComputeTargetNotFound' in e.message:
            print('Data factory not found, creating...')
            provisioning_config = DataFactoryCompute.provisioning_configuration(location='eastus')
            data_factory = ComputeTarget.create(workspace, factory_name, provisioning_config)
            data_factory.wait_for_completion()
            return data_factory
        else:
            raise e
            
data_factory_compute = get_or_create_data_factory(ws, data_factory_name)

print("setup data factory account complete")
