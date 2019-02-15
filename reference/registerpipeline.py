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
ds = ws.get_default_datastore()

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

register = PythonScriptStep(name="Register model for deployment",
                         script_name="register.py", 
                         compute_target=aml_compute,
                        #  inputs=[model],
                        #  outputs=[modelId], 
                         source_directory=project_folder)
steps = [register]

pipeline1 = Pipeline(workspace=ws, steps=steps)
print ("Pipeline is built")

pipeline1.validate()
print("Pipeline validation complete")


pipeline_run1 = Experiment(ws, 'justregister').submit(pipeline1, regenerate_outputs=True)
print("Pipeline is submitted for execution")
