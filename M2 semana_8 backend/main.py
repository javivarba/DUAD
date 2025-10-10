import redis


redis_client = redis.Redis(
    host="redis-18507.c241.us-east-1-4.ec2.redns.redis-cloud.com",
    port=18507,
    password="yUUJ4nQ8XjKiX36aAl7O0a5RtIqizYlV",
)

try:
    connection_status = redis_client.ping()
    if connection_status:
        print("Connected to Redis!")
    else:
        print("The connection to Redis was unsuccessful!")
except redis.ConnectionError as ex:
    print("An error ocurred while connecting to Redis: ", ex)

value = redis_client.get("full_name")
print(value.decode('utf-8'))