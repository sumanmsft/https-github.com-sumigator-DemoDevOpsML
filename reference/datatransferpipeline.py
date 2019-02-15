from azureml.pipeline.core import Pipeline, PipelineData, StepSequence
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.steps import DataTransferStep
from azureml.pipeline.core import PublishedPipeline
from azureml.pipeline.core.graph import PipelineParameter
from azureml.core import ScriptRunConfig
from azureml.core import Workspace, Run, Experiment, Datastore
from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget, DataFactoryCompute
from azureml.data.data_reference import DataReference

aml_compute_target = "cpu"
project_folder = '.'

ws = Workspace.from_config()


# Runconfig
from azureml.core.runconfig import CondaDependencies, RunConfiguration
cd = CondaDependencies.create(pip_packages=["sklearn", "azureml-defaults"])
amlcompute_run_config = RunConfiguration(conda_dependencies=cd)

# Make sure the compute target exists
try:
    aml_compute = AmlCompute(ws, aml_compute_target)
    print("found existing compute target.")
except:
    print("compute target not found. exiting")

#Data transfer example

data_factory_name = "adf"
data_factory_compute = DataFactoryCompute(ws, data_factory_name)

# For model reproducibility, we want to ensure that we preserve the images we're actually using to train from the larger data lake

source_ds = Datastore.get(ws, 'amlvdaik14969151586')
dest_ds = ws.get_default_datastore()

orig_images = DataReference(
    datastore=source_ds,
    data_reference_name="origin_images",
    path_on_datastore= '')

dest_images = DataReference(
    datastore=dest_ds,
    data_reference_name="destination_images",
    path_on_datastore= 'my_training_data')

transfer_images = DataTransferStep(
    name="transfer_images",
    source_data_reference=orig_images,
    destination_data_reference=dest_images,
    compute_target=data_factory_compute)

steps = [transfer_images]

print("Step lists created")

pipeline1 = Pipeline(workspace=ws, steps=steps)
print ("Pipeline is built")

pipeline1.validate()
print("Pipeline validation complete")

pipeline_run1 = Experiment(ws, 'justdatatransfer').submit(pipeline1)
print("Pipeline is submitted for execution")