FROM python

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051
EXPOSE 50052
EXPOSE 50053
EXPOSE 50054
EXPOSE 50055
EXPOSE 50056
EXPOSE 50057
EXPOSE 50058

# run the command
CMD ["python", "-u", "./wait_room_server.py"]
