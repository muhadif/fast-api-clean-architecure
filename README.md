# Fast API with Clean Architecture
# Overview
This project use FastAPI as web framework in python. Also use several library for help me for deployment process
1. **Python 3.10**, main programing language
2. **FastApi**, web framework
3. **Atlas**, migration tool, can create migration from model in python and run seamless
4. **sqlalchemy**, gorm for database, support many databases, easy understanding
5. **cacheout**, memory cache for python, can be replaced with other cache like redis
6. **pytest**, testing framework for python, easy setup, easy implementation and have huge type of reporting
## Run application
Run server with `uvicorn`
1. Setup _.env_
```
ENV=development
DB=mysql
DB_USER=fastapi
DB_PASSWORD=fastapi
DB_HOST=localhost
DB_PORT=3309
```
3. Run database migration,
```
atlas migrate apply --url=mysql://fastapi:fastapi@localhost:3309/fastapi
```
2. Run application
```
uvicorn app.main:app
```
3. API documentation can be open on _/docs_ with https://www.usebruno.com/

## Running Test
1. Makesure PYTHONPATH at right directory
```
export PYTHONPATH=$PWD
```
2. Run with `pytest`
```
pytest tests
```

## TODO Performance Tuning
This is repository consist MVP for python web with FastAPI framework, we have some TODO to this project:
### System Architecture
![img.png](system-architecture.png)
1. **Microservice Architecture**, divide the module as services will help the application to handle huge request with scalable service, 
   We can scale particular service that have huge request, it can by automatically
2. **Load balancer**, ton of request need load balancer to filter the request and make sure all of thing in internal service run well
3. **Communication**, for service communication it can be synchronous with REST/GRPC and for asyncronouse we can use broker like Kafka or Pubsub
4. **Database**, Huge service will need hug database also, we need something like clustering SQL for handling ton of query
5. **Redis**, Redis only have one core, but for handling huge request we can use redis cluster

#### Performance Tuning improvement
For handling ton of request, we need make sure the database SQL and cache can handle it. So what we need to do:
1. **Service**, use asynchronous for request that can be handle with it
2. **Service**, implement async await for huge transaction data
2. **Database**, start with 3NF design database
3. **Database**, make sure for each query filter (where) use indexing table
4. **Database**, consider partitioning and sharding
5. **Cache**, use preload cache like using worker for example scheduled every 1day
6. **Load balancer**, implement rate limiter to make sure the internal service or resource not broke, but make sure we already did load test to make sure TPS of the services 
