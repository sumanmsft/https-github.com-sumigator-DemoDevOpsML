# Data 

# Data Parameters
A data parameter should have a DataReference as the default value of the parameter (which specifies datastore and data path).  To use this as input to the script, you create a tuple with the data parameter and a DataPathComputeBinding, which specifies the input mode (defaults to "mount").  The code would look like the following:
 
 ```
from azureml.data.datapath import DataPath, DataPathComputeBinding
from azureml.pipeline.core.graph import PipelineParameter
 
video_path = DataPath(datastore=my_datastore, path_on_datastore="dne.mp4")
video_path_param = (PipelineParameter(name="video_path", default_value=video_path), DataPathComputeBinding())
 
preprocess_video_step = PythonScriptStep(
    name="preprocess video",
    script_name="preprocess_video.py",
    arguments=["--input-video", video_path_param,
               "--output-audio", ffmpeg_audio,
               "--output-images", ffmpeg_images,
              ],
    compute_target=cpu_cluster,
    inputs=[video_path_param],
    outputs=[ffmpeg_images, ffmpeg_audio],
    runconfig=ffmpeg_run_config,
    source_directory=project_folder,
    allow_reuse=False
)
 
pipeline = Pipeline(... )

pipeline_run = Experiment(ws, 'style_transfer_mpi_param').submit(
    pipeline, pipeline_params={'video_path': DataPath(datastore=my_datastore, path_on_datastore="dne.mp4")})
```
