from kafka import KafkaProducer
from kafka.errors import KafkaError
import cv2
from datetime import datetime
import numpy as np
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# vidcap = cv2.VideoCapture('nguoianhHoangTung.mp4')
# success,image = vidcap.read()
count = 0

start_date = datetime.now()

# while success:
#     success,image = vidcap.read()
#     if success == False:
#         break
#     count += 1

#     ret, buffer = cv2.imencode('.jpeg', image) #buffer type: np array
#     print(buffer.shape)
#     future = producer.send('detection', buffer.tobytes())
#     try:
#         record_metadata = future.get(timeout=10)
#     except KafkaError:
#         log.exception()
#         pass
#     print ("frame: " + str(count) + ",topic name: " + str(record_metadata.topic) + ",partition: " + str(record_metadata.partition) + ",offset: " + str(record_metadata.offset))

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    if not ret:
        print("Camera not working")
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()
    future = producer.send('detection', value=frame_bytes)
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        log.exception()
        pass
    print ("frame: " + str(count) + ",topic name: " + str(record_metadata.topic) + ",partition: " + str(record_metadata.partition) + ",offset: " + str(record_metadata.offset))

    cv2.imshow('The stage is representing...', frame)
    count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if (count==50):
        break

camera.release()
cv2.destroyAllWindows()
end_date = datetime.now()
print(end_date - start_date)