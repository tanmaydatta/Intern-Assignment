This is the Back End Developer Internship Assignment.  

# Pre-requisites
- [Redis Stable](http://redis.io/topics/quickstart)
- Python 2.7 with python-dev

# Instructions
- `pip install -r requirements.txt`
- Run the server with `gunicorn --workers 5 --bind 0.0.0.0:5000 wsgi`
- You can set the number of workers as per need (for concurrent requests)
- Make the requests at http://localhost:5000/
