FROM python:3.10-slim-buster

COPY . /luiza_labs_desafio

WORKDIR /luiza_labs_desafio

COPY requirements_test.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pytest coverage
RUN pip install -r requirements_test.txt

CMD ["python3", "-m", "pytest", "--junitxml=pytest_save_reports/pytest_report.xml"]