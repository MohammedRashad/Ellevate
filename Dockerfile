FROM python:3.10-slim
EXPOSE 8501
WORKDIR /usr/src/app
COPY . . 
#COPY streamlit_app.py ./
#RUN apt-get update &&  apt-get install python3-pip
RUN pip3 install -r requirements.txt
#COPY . .
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["chainlit", "run"]
CMD ["ui.py"]
