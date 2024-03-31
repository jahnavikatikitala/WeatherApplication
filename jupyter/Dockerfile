# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install Jupyter
RUN pip install --no-cache-dir jupyter

# Create a working directory
WORKDIR /notebooks

# Expose the port for Jupyter notebook server
EXPOSE 8887
RUN pip install pandas
RUN pip install ipython-sql
RUN pip install psycopg2-binary


# Run Jupyter notebook server
CMD ["jupyter", "notebook", "--ip='*'", "--port=8887", "--allow-root"]

