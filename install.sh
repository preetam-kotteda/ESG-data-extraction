eval "$(conda shell.bash hook)"
conda create -n ESG python=3.8
conda activate ESG
pip3 install -r requirements.txt
conda deactivate