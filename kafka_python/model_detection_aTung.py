from PIL import Image, ImageDraw 
from io import BytesIO
from confluent_kafka import Producer, Consumer, KafkaError
import numpy as np
import cv2
import torch

bootstrap_servers = 'localhost:9092'
topic_in = 'detection'
group_id = 'detection'

topic_out = 'represent'

consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}

producer_config = {
    'bootstrap.servers': bootstrap_servers
}


producer = Producer(producer_config)

consumer = Consumer(consumer_config)
consumer.subscribe([topic_in])

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    

try:
    while True:
        msg = consumer.poll(1.0)  # Adjust the polling interval as needed
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
        else:
            stream = BytesIO(msg.value())
            image_cv2 = cv2.imdecode(np.frombuffer(msg.value(), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            stream.close()

            # Process the image using the loaded model
            results = model(image_cv2)
            result_string = str(results.pandas())
            print(result_string)

            # Send the result_string to the output topic
            producer.produce(topic_out, value=result_string.encode('utf-8'))

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    producer.flush()
