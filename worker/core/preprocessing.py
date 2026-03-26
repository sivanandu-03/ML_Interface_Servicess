def preprocess_features(raw):
    return {
        "sepal_length": float(raw["sepal_length"]),
        "sepal_width": float(raw["sepal_width"]),
        "petal_length": float(raw["petal_length"]),
        "petal_width": float(raw["petal_width"])
    }
