FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 8510

RUN apt update
RUN apt install -yqq git
RUN apt-get install -y g++
RUN pip install pylint==3.2.2 mypy==1.10.0 pandas-stubs==1.2.0.57

COPY . /app
CMD ["streamlit", "run", "show_mermaid.py", "--server.port", "8510", "--server.address", "0.0.0.0"]
