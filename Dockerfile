# Use a Windows Server Core base image
FROM mcr.microsoft.com/windows/servercore:ltsc2019 

# Set the working directory to /app
WORKDIR /chabot
COPY requirements.txt chabot_codes/requirements/requirements.txt
COPY app.py /chabot/chabot_codes/app.py
COPY utils.py /chabot/chabot_codes/utils.py
COPY ./storage /chabot/chabot_codes/storage
COPY ./data /chabot/chabot_codes/data 

# Install Python and required packages
RUN powershell-Command \
    $ErrorActionPreference 'Stop'; \
    Invoke-MebRequest -Uri https://www.python.org/ftp/python/3.18.e/python-3.10.0-amd64.exe -OutFile python-3.10.0-amd64.exe; \
    Start-Process python-3.10.0-amd64.exe -ArgumentList '/quiet InstallAllUsers-1 PrependPath-1' -Wait; \
    Remove-Item python-3.10.0-amd64.exe;

# Install pip
RUN powershell-Command \
    $ErrorActionPreference = 'Stop'; \
    Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py; \
    python get-pip.py; \
    Remove-Item get-pip.py;

# Install required packages
RUN pip install -r chabot_codes/requirements/requirements.txtS
RUN mkdir logs

# Expose port 
EXPOSE 8080
ENTRYPOINT [ "powershell.exe" ]

# Start the API using uvicorn
CMD ['uvicorn', 'chabot_codes.main:app', '--host','0.0.0.0','--port','8080'.'--workers','2']