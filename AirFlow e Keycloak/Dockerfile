FROM apache/airflow:3.0.6

# Switch to root to install packages
USER root

# Switch back to airflow user
USER airflow

# Install the Keycloak provider
RUN pip install --no-cache-dir \
    python-keycloak \
    apache-airflow-providers-keycloak
