FROM apache/airflow:2.9.2

# INSTALL BASE packages

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/airflow/logs/scheduler/2024-06-28 \
  ; chown -R airflow /opt/airflow/logs \
  ; chmod 777 -R /opt/airflow

USER airflow

# COPY package references file to the container
COPY requirements.txt /
# INSTALL AIRFLOW Python packages
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

COPY --chown=airflow:root test_dag.py /opt/airflow/dags

ENV AIRFLOW__CORE__LOAD_EXAMPLES=false

