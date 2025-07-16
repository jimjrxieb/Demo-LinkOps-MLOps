FROM python:3.11-slim

WORKDIR /app

COPY dataset/ dataset/
COPY training_orbs/ training_orbs/
COPY train_classifier.py infer.py utils.py* ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "infer.py"] 