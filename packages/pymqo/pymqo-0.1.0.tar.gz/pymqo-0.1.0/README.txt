# pymqo
Python Message Queue Object

# Example

## Consumer

```python
def callback(body):
    print(" [x] %r" % body)

obj = RabbitMQObject(
    ampq_url='amqp://rabbitmq:rabbitmq@localhost/localhost',
    exchange='logs',
    exchange_type='fanout',
    routing_key='',
    consume_callback=callback
)
message = 'Hello'
obj.connect()
obj.basic_consume()
```


## Publisher

```python
obj = RabbitMQ(
    ampq_url='amqp://rabbitmq:rabbitmq@localhost/localhost',
    # host='localhost',
    exchange='logs',
    exchange_type='fanout',
    routing_key=''
)
message = 'Hello'
obj.connect()
obj.basic_publish(message=message)
obj.close()

```