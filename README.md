# Selenium Test Automation Framework 

Selenium (Page Object Model) Automation Framework using PyTest

**Browser supported :** Chrome , FireFox, IE 

SETUP 

Steps to Set up the Framework on Local Repository
  1. Checkout the repository from GIT by below command

     -- git clone https://github.com/amits0003/PytestAutomationAssignment.git

  2. open the repository in PyCharm / any other IDE and then navigate to Terminal

  3. Create a virtual Environment by typing below command in the terminal

    python3 -m venv venv
     or,
    python -m venv venv

    (any of the above command will run as per sysytem's python installation property


    There are two ways to install the required libraries into the virtual environment
      1. Close the terminal and then again open the terminal (a virtual environment should be loaded in the terminal already)
          then type the below command

    pip install -r requirements.txt


      2. type the below command to install the libraries in to the  virtual environemnt

         python setup.py install
         or
         python3 setup.py install

Now the Environment set up is completed...


Steps to Run the Test Scripts - 

Pre-Requisites - Make Sure that the Python 3.8 is installed in the Local System.

1. Clone the Directory to a Folder
2. Activate the Virtual Environment using "python -m venv venv"
3. activate terminal to the root folder of the project.
4. Install the requirements using "pip install -r requirements.txt"

# There are two ways to run the test Scripts 

** Running the individual test Scripts **
1. navigate to the test Script folder
2. Run the individual test scripts using "pytest test_DDLCommands.py --html='output_1.html' " 
3. similarly run the test from all the other files


** Running all the test Scripts using run_test.py file **

1. Navigate to the testRunner folder in command terminal
2. run the command "python run_test.py"

this way all the test will be executed and their html report will be saved to the test folder.








