import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def train_and_save(model_path='ml_model/model.pkl'):
    iris = load_iris()
    X, y = iris.data, iris.target
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=50, random_state=42))
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, model_path)
    print('Saved model to', model_path)


if __name__ == '__main__':
    train_and_save()
