# **Project Startup**

This guide outlines the steps to set up a new project using FastAPI.

## **Prerequisites**

Before you begin, ensure you have the following prerequisites:

- Python installed on your system
- Pip (Python package manager) installed
- Basic understanding of virtual environments (optional but recommended)

## **Setup Instructions**

### **Mac**
1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install FastAPI and Uvicorn:
    ```bash
    pip install fastapi uvicorn
    pip install "uvicorn[standard]"
    ```


### **Windows**
1. Create a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

2. Install FastAPI and Uvicorn:
    ```bash
    pip install fastapi uvicorn
    pip install "uvicorn[standard]"
    ```

## Time to Install FastAPI
In order for us to interact with our fastAPI application, we are going to need a server. So if you imagine client sending some sort of request to API, a message directly to our FastAPI application, FastAPI wont know how to handle that message.
- for example typically send a http get request to FastAPI application, fastAPI doesnt actually know how to handle that

So the idea is we have a server package wrapped up around fastAPI: HERE we are gona be utilizing UVICORN
- this is a lightweight and asynchronous server gateway interface, it will get the client request and translate it into something that fastAPI can actually handle


