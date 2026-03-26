import joblib


class MLService:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        if self.model is None:
            self.model = joblib.load(self.model_path)
        return self.model

    def is_model_loaded(self):
        return self.model is not None

    def predict(self, processed_features: dict):
        model = self.model
        if model is None:
            raise RuntimeError('Model not loaded')

        # features are expected as a dict with numeric values listed in typical iris order
        feature_order = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        vector = [[float(processed_features[field]) for field in feature_order]]
        prediction = model.predict(vector)
        return int(prediction[0])
