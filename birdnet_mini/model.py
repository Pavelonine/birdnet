import operator

import numpy as np
from pathlib import Path

try:
    import tflite_runtime.interpreter as tflite
except ModuleNotFoundError:
    from tensorflow import lite as tflite


class Model:
    def __init__(self, model_path, labels, num_threads=1):

        self._interpreter = tflite.Interpreter(model_path=model_path, num_threads=num_threads)
        self._interpreter.allocate_tensors()
        input_details = self._interpreter.get_input_details()
        output_details = self._interpreter.get_output_details()
        self._output_layer_index = output_details[0]["index"]
        self._input_layer_index = input_details[0]["index"]
        self.labels = labels

    def _load_meta_model(self):
        raise NotImplementedError

    def predict(self, chunk):

        # Make sure the data is in the right format
        # the models has the batch size as the first dimension
        # we are only using one chunk at a time - we need to wrap it in list such that we get
        # dimensions [1, num_samples]
        batch_data = np.array([chunk], dtype="float32")

        # Set the input tensor
        self._interpreter.set_tensor(self._input_layer_index, np.array(batch_data, dtype="float32"))

        # run the model
        self._interpreter.invoke()

        # Retrieve the output tensor
        prediction = self._interpreter.get_tensor(self._output_layer_index)

        # Apply sigmoid function to get confidence score for each class (they do not sum up to 1 though)
        prediction = self._flat_sigmoid(np.array(prediction))

        # Check if the prediction has the right shape
        assert prediction.shape[1] == len(self.labels)

        # Assign scores to labels - we use prediction[0] because we only have one batch entry
        p_labels = zip(range(len(self.labels)), self.labels, prediction[0])

        # Sort by score in ascending order
        p_sorted = sorted(p_labels, key=operator.itemgetter(2), reverse=True)

        # return top 5 predictions
        return list(p_sorted)[:5]

    @staticmethod
    def _flat_sigmoid(x, sensitivity=-1.0):
        return 1 / (1.0 + np.exp(sensitivity * np.clip(x, -15, 15)))
