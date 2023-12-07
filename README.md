# Creating an API with Python and FastAPI

This is a microblog project inspired by the LINUXtips training, "Creating API with Python and FastAPI."

## Features

### Users
- User registration
- User authentication
- Follow other users
- Profile with bio and listing of posts, followers, and following

### Posts

- Create a new post
- General post listing (home)
- Listing of posts from followed users (timeline)
- Posts can be replies to other posts

## Requirements
- Python 3.10
- Docker & Docker compose

## Installation

As this is an API running inside a container, to install the project, execute the following command:

```Bash
docker build -f Dockerfile.dev -t pamps:latest .
```
This command builds the container where the API will be running. The next step is to run it using:
```Bash
docker compose up
```
This command starts the API + the database inside the container, using Docker Compose as the container orchestrator.

To ensure everything works correctly, set the `SECRET_KEY` within the `secrets.toml` file. Create the `secrets.toml` file in the root of the repository and add the following lines:

```Python
[development]
dynaconf_merge = true

[development.security]
SECRET_KEY = "YOURSECRETKEY"  # You can change the value of the key to anything you prefer.
```

## Accessing the API
To access the API, simply go to the local address on your PC and port 8000, which is configured in the Dockerfile.dev file in the root of the repository.
```
localhost:8000/docs
```
## Additional Features

- Edit posts
- Remove posts
- Likes on posts
- Front-end
