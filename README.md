# LocationDetectorServer
*Note: Instructions are running on Windows Command Prompt.* 
- First, move to the working directory and clone the repository.  
`git clone https://github.com/tlphat/LocationDetectorServer.git`
- Go to folder **LocationDetectorServer**.  
`cd LocationDetectorServer`
- Next, we check if `virtualenv` has been installed.  
`virtualenv --version`
- If not, install it using pip install command. Otherwise, we skip this step.  
`pip install virtualenv`
- Create the new virtual environment, then activate it.  
`virtualenv venv`  
`venv\Scripts\activate`
- Then, we install Django and Pillow.  
`python -m pip install django`  
`python -m pip install pillow`
- Install DELF following the instructions here https://github.com/tensorflow/models/blob/master/research/delf/INSTALL_INSTRUCTIONS.md
- Then, we can go to folder **myproject** and run the server.  
`cd myproject`  
`python manage.py runserver 0.0.0.0:8000`
- To stop the server, press Ctrl+C.  
- To deactivate the virtual environment: `deactivate`
