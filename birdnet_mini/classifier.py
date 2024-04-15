import datetime
import queue
import time
import random
from queue import Queue
from threading import Thread


class Model:
    def __init__(self, model_path=None):
        pass

    def predict(self, samples):
        pass


class BirdClassifier (Thread):
    def __init__(self, sample_queue: Queue, result_queue: Queue):
        super(BirdClassifier, self).__init__()
        self._model = Model()
        self._sample_queue = sample_queue
        self._result_queue = result_queue
        self._interrupted = False

    def interrupt(self):
        self._interrupted = True

    def run(self):
        while not self._interrupted:
            try:
                chunk = self._sample_queue.get(timeout=0.1)
            except queue.Empty:
                continue
            time.sleep(1)
            # we are using a very simple protocol here to reduce the amount of data sent via serial / Mioty
            # generate random classification result
            class_id = random.randint(0, 6000)
            bird_confidence = random.random()
            random_lat = random.uniform(-90, 90)
            random_lon = random.uniform(-180, 180)
            data = {
                "class_id": class_id,
                "confidence": bird_confidence,
                "lat": random_lat,
                "lon": random_lon,
                "timestamp": datetime.datetime.now().timestamp()
            }
            self._result_queue.put(data)
