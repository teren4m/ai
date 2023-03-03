conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
python.exe -m pip install --upgrade pip
pip install "tensorflow<2.11" 
python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"