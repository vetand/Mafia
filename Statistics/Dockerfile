# Using lightweight alpine image
FROM python
RUN apt-get update -y

# Defining working directory and adding source code
WORKDIR /usr/src/app

COPY . .

# Installing packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Start app
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]