import datetime
import queue
import time
import random
from queue import Queue
from pathlib import Path
from threading import Thread


class BirdClassifier (Thread):
    def __init__(self, model, sample_queue: Queue, result_queue: Queue):
        super(BirdClassifier, self).__init__()
        self._model = model
        self._sample_queue = sample_queue
        self._result_queue = result_queue
        self._model = model
        self._interrupted = False

    def interrupt(self):
        self._interrupted = True

    def run(self):
        while not self._interrupted:
            try:
                chunk, timestamp, lat, long = self._sample_queue.get(timeout=0.1)
            except queue.Empty:
                continue
            prediction = self._model.predict(chunk)
            class_id = prediction[0][0]
            class_label = prediction[0][1]
            confidence = prediction[0][2]
            print(f"[classifier] Top prediction {class_label}({class_id}), with confidence: {confidence:.02f}")
            data = {
                "class_id": class_id,
                "confidence": float(confidence),
                "lat": lat,
                "lon": long,
                "timestamp": timestamp
            }
            self._result_queue.put(data)
