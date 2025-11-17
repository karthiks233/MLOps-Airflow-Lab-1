FROM apache/airflow:2.10.0

USER root

# Copy the file owned by root
COPY requirements.txt /tmp/requirements.txt

# Change ownership so airflow user can access it
RUN chown airflow: /tmp/requirements.txt

# Drop privileges
USER airflow

# Install Python packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt
