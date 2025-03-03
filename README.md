# ITC_BD
# Git Workflow for Personal, Development, and Main Branches
The workflow follows a progression from the personal branch to development, and finally to the main branch.

# Best Practices

* Always pull the latest changes before starting new work into personal forked repo.

* Use meaningful commit messages.

* Test thoroughly before merging into development.

* Test development branch thoroughly before merging into main.

* Resolve merge conflicts carefully.

Following this workflow ensures a structured development process while maintaining code stability. Happy coding!

the project setup:

my_python_project/       
│── src/                   
│   ├── __init__.py          # Package initializer
│   ├── main.py              # Main script
│   ├── tfl_status.py        # API call logic
│   ├── utils.py             # Helper functions
│── tests/                   
│   ├── test_tfl_status.py   # Unit test for TfL API
│── requirements.txt         # Dependencies (requests, python-dotenv)
│── README.md                # Project description
│── .gitignore               # Ignore unnecessary files
│── .env                     # API credentials (DO NOT COMMIT)
│── venv/                    # Virtual environment





1. please run the requirements.txt file before progressing with the project.
    the command is pip install -r requirements.txt




WHAT IS HAPPENING IN THE CODE AND IT'S EXPLANATION:

This python project will gather data from the TFL API
The tfl_status.py file fetches data from tfl API using 'requests' it stores the data as JSON
When tfl_status.py fetches the JSON data from the TfL API, it will be stored locally on your machine before being uploaded to HDFS. By default, the file tfl_data.json will be saved in the root of your project directory (same location where you run your script).

After saving the data locally, we now need to upload it to HDFS for this we have the hdfs_handler.py We need to have hadoop running in our system before it can be saved to hdfs otherwise the code will fail. If you are working on your local machine, you need Hadoop installed and HDFS running.

