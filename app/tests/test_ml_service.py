import os
import joblib
from app.services.ml_service import MLService


def test_ml_service_load_and_predict(tmp_path):
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    iris = load_iris()
    model = Pipeline([('scaler', StandardScaler()), ('rf', RandomForestClassifier(n_estimators=1, random_state=42))])
    model.fit(iris.data, iris.target)

    model_file = tmp_path / 'model.pkl'
    joblib.dump(model, model_file)

    service = MLService(str(model_file))
    service.load_model()

    processed = {
        'sepal_length': 5.1,
        'sepal_width': 3.5,
        'petal_length': 1.4,
        'petal_width': 0.2,
    }
    pred = service.predict(processed)
    assert isinstance(pred, int)
    assert pred in [0, 1, 2]
