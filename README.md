Setup and run in a virtual environment:
```
python3 -m venv venv
venv/bin/python3 -m pip install --upgrade pip
venv/bin/pip install -r requirements.txt
venv/bin/python main.py
venv/bin/python main.py destroy
```


| File  | Functionality |
| ------------- | ------------- |
| main.py | Creates an S3 Bucket static site  |
| main-k8s.py  | Creates a nginx pod in k8s  |