conda create --name aind-cv python=3.5 numpy
source activate aind-cv
pip install tensorflow==1.1.0
pip install keras -U
KERAS_BACKEND=tensorflow
pip install -r requirements.txt
