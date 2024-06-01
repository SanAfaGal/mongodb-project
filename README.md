
## Instructions to Run:

1. Clone the repository:

```
git clone https://github.com/SanAfaGal/mongodb-project
```

2. Navigate to the project directory:
```
cd mongodb-project
```

3. Create a virtual environment and install packages:
```
pip install -r requirements.txt
```

4. Ensure you have the MongoDB Atlas connection string in the .env file:
```
MONGODB_URI='<str>'
```

5. Create 3 collections in the 'event_management' database:
```
users
events
comments
```

## Make sure to

- Include your IP address in the IP access list by selecting the Network Access tab.
- Create a user and password to access the database.
- Update the correct username and password in the MONGODB_URI environment variable.

6. Run the program in the terminal:
```
uvicorn app:app
```
## Usage and Examples


To view the documentation and test the endpoints, go to the following URL once the project is running:

```
http://127.0.0.1:8000/docs
```

