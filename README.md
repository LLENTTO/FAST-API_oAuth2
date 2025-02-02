# This is an example of  FAST-API server

### This programm provides an example of simple running server on FAST-API backend library. 
<hr />

### Core concepts of server

- OAuth2 x JWT integration for authentication
- User 1000 handle
- Handling database with NoSQL MongoDB server

<hr />

### Routes
- /token - checks for avialable session
- /check - middleaware for connection checking

<hr />

# IMPORTANT PREQS

- Installed Python
- Installed Docker (Docker desktop is optional)
- Installed Mongo (MongoDB compass is optional)

### <i>To run the software you should install all the required documents located in [requirements](./requirements.txt) file </i>

### <i>Installation guide:</i>
    - Check for versions: python/docker --version
    - git clone https://github.com/LLENTTO/FAST-API_oAuth2
    - CD to the installed folder

### Running with docker:
-   ```docker-compose up --build```

### Running on local machine:
-   ```python -m venv myenv```
<i>If using windows powershell</i> - ```myenv\Scripts\activate.psl```
<i>If using windows command prompt</i> - ```myenv\Scripts\activate```
-   ``` pip install -r requirements.txt ```
-   ```cd app```
-   ```uvicorn server:app --reload```

<hr />

### <i>To run the server you should create your mongoose database with schema is already existed on the repository</i>

### Instruction for setting up database
- Log In/Sign up on [MongoDB](https://account.mongodb.com/account/login) atlas platform
- Choose any plan and create the server
- Add the URI to [.env](./.env) file

### OR

- Run MongoDB server on local machine

### OR

- Simply run ```docker-compose up```

<hr />

Created by GitHub LLENTTO