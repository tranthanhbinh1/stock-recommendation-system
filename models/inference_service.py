import bentoml
import numpy as np
from bentoml.io import NumpyNdarray


runner = bentoml.pytorch.get("LSTM-Stock-Prediction").to_runner()

svc = bentoml.Service(name="LSTM-test-service", runners=[runner])

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def predict(input: np.ndarray) -> np.ndarray:
    result = svc.predict.run(input)
    return result