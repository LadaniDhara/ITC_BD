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
