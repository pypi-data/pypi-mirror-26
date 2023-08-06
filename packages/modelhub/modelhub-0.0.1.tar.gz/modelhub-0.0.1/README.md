# Modelhub 
a cli to manage your models.

It take a TensorFlow SaveModel file, upload it with version and meta info. And checkout will download it to local.


info model_name [version_number]

create model_name -m "comment"

submit model_name -m "comment" [–batching_config=batching_config.txt] model_path

checkout model_name [version_number]

deploy model_name [version_number] [CPU/GPU] [online/offline] [instance-number] [offline]

version control 

python API

get model path by model name [and version]

checkout model

