from PIL import Image, ImageDraw 
from io import BytesIO
from confluent_kafka import Producer, Consumer, KafkaError
import numpy as np
import cv2
import torch

bootstrap_servers = 'localhost:9092'
producer_config = {
    'bootstrap.servers': bootstrap_servers
}
producer = Producer(producer_config)

topic = 'detection'
group_id = 'detection'
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_config)
consumer.subscribe([topic])

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

for message in consumer:
    stream = BytesIO(message.value)
    image_cv2 = cv2.imdecode(np.frombuffer(message.value,'u1') , cv2.IMREAD_UNCHANGED)
    stream.close()
    # image.show()
    results = model(image_cv2)
    result_string = str(results.pandas())
    print(result_string)
    output_image = results.render()[0]

    # push to frontend
    ret, buffer = cv2.imencode('.jpeg', output_image)
    future = producer.send('represent', bytes(result_string, "utf-8"))
    
    # Display the image
    cv2.imshow('Received Image', output_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
