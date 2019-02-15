from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget
from azureml.core import Workspace

ws = Workspace.from_config()
aml_compute_target = "cpu"

# Provision AML compute
provisioning_config = AmlCompute.provisioning_configuration(vm_size = "STANDARD_D2_V2",
                                                            min_nodes = 1, 
                                                            max_nodes = 4)    
aml_compute = ComputeTarget.create(ws, aml_compute_target, provisioning_config)
aml_compute.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)