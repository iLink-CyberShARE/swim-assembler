# SWIM-Assembler Service
Scenario input creation service for model-to-model workflows on SWIM.

## Features
+ Assemble SWIM input scenarios for model consumption.
+ Load default data values if inputs values are not defined.
+ Map inputs with incoming from other model executions.

## Build and Run

### Option 1: Docker Compose File
This setup is recommended for production environment.   

1. Download the docker-composer.yml file to a path in your machine.   
2. Install Docker and Docker composer on your target machine.   
3. Setup your docker account at: https://www.docker.com/get-started   
4. Configure the docker-composer file with your own app settings.   
5. Run docker compose: $docker-compose up   
5a. Use -d option o the composer command to run on the background.    
6. swagger docs will be available at http://localhost:5020/swim-assembler/docs/ 


### Option 2: Build Docker Container
This setup is recommended for testing environment.   

1. Download this repository into a folder on your machine.
2. Install Docker and Docker composer on your target machine.
3. Setup your docker account at: https://www.docker.com/get-started
4. Using a command line or terminal navigate to the base path of the project.
5. Build the image: $docker build -t swim-hs:latest .
6. Run the container: $docker run dockeruser/swim-assembler
7. Swagger docs available at http://localhost:5002/swim-assembler/docs/

### Option 3: Native
This setup is recommended for development environment.       

1. Install Python 3 and pip on your machine.
2. Create new virtual python environment: $py -m venv env 
3. Activate virtual environment. $env\Scripts\activate
4. Update the pip repository: $update pip
5. Install required packages: $py -m pip install -r requirements.txt
6. Modify the file /app/main/config with your local settings and database connections on the development settings.
6. Run service on localhost: $py manage.py run  // run webservice on localhost (windows)
7. swagger docs will be available at http://localhost:5000/swim-assembler/docs/

## Dependencies:
This service requires previous deployment of the following artifacts. See documentation for more information.

1. SWIM Broker Service
2. SWIM Workflow Database

## Testing
Commands for testing assembly methods:

> py manage.py simple_assemble // run a simple assemble operation
> py manage.py complex_assemble // run a complex assemble operation

### Documentation

This service forms part of the SWIM orchestration services for additional documentation refer to:   
[SWIM Broker](https://water.cybershare.utep.edu/resources/docs/en2/backend/swim-broker/)

## Contributors
Luis Garnica Chavira    

## Acknowledgements
This material is based upon work supported by the National Science Foundation (NSF) under Grant No. 1835897.   

Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.  

## License
GNU General Public License 3.0

## Copyright   
© 2022 - University of Texas at El Paso (SWIM Project).   