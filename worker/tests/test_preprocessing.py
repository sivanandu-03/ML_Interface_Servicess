from worker.core.preprocessing import preprocess_features


def test_preprocess_features():
    raw = {
        'sepal_length': '5.1',
        'sepal_width': '3.5',
        'petal_length': '1.4',
        'petal_width': '0.2',
    }

    processed = preprocess_features(raw)
    assert processed['sepal_length'] == 5.1
    assert processed['sepal_width'] == 3.5
    assert processed['petal_length'] == 1.4
    assert processed['petal_width'] == 0.2
