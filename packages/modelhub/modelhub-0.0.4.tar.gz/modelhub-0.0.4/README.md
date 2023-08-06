# Modelhub 

A CLI tool to manage your models.

## Commands

It takes a TensorFlow SaveModel file, uploads it with version and meta info, and checkouts it to local.

\- info model_name[@version_number]

\- create model_name -m "comment"

\- submit model_name -m "comment" [–batching_config=batching_config.txt] model_path

\- checkout model_name[@version_number]

\- deploy model_name[@version_number] [CPU/GPU] [online/offline] [instance-number] [offline]



##Python API
pass
get model path by model name [and version]

checkout model