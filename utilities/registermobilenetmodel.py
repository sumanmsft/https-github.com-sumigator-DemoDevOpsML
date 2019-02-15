from azureml.core import Workspace
from azureml.core.model import Model
import os
import tarfile
import urllib
import sys


def download_and_extract(data_url, dest_directory):
  """Download and extract model tar file.

  If the pretrained model we're using doesn't already exist, this function
  downloads it from the TensorFlow.org website and unpacks it into a directory.

  Args:
    data_url: Web location of the tar file containing the pretrained model.
  """
  print(dest_directory)
  if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)
  filename = data_url.split('/')[-1]
  filepath = os.path.join(dest_directory, filename)
  urllib.request.urlretrieve(data_url, filename)  
  tarfile.open(filepath, 'r:gz').extractall(dest_directory)
  

model_dir = os.path.curdir
model_uri = 'https://raw.githubusercontent.com/rakelkar/models/master/model_output/mobilenet_v1_1.0_224_frozen.tgz'
download_and_extract(model_uri, model_dir)


ws = Workspace.from_config()
Model.register(ws,'imagenet_2_frozen.pb','mobilenet.imagenet',tags={'dataset':'imagenet_2'})