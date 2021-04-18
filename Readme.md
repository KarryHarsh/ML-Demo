## Create a new conda environment
* open anaconda prompt

```bash
conda create -n mlenv python=3.7 -y
```
* activate the envirnoment

```bash
conda activate mlenv
```
* Install requirements using requirements.txt

```bash
pip install -r requirements.txt
```

* open the Notebook in same virtual env

```bash
jupyter notebook
```

* open new prompt and run change to virtual env like above
* change the directory where project got downloaded.

```bash
cd ./ml-demo
```

* Start MLflow tracking server locally

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root mlruns/ --host 127.0.0.1 --port 5000
```

* Run the experiments

## To run flask application

* change directory to MlApp application folder using anaconda prompt or any IDE.

Note: If using IDE set the interpreter and executable of your virtual env and conda env respectively

* Run Flask app using below command.
```bash
python .MLApp/Apps/MLApps.py
```  



