"""Tests scikit-learn's DictVectorizer converter."""

import unittest
from sklearn.feature_extraction import DictVectorizer
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import (
    DictionaryType,
    StringTensorType,
    FloatTensorType,
    Int64TensorType,
)
from skl2onnx.common.data_types import onnx_built_with_ml
from test_utils import dump_data_and_model


class TestSklearnDictVectorizerConverter(unittest.TestCase):
    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    def test_model_dict_vectorizer(self):
        model = DictVectorizer()
        data = [{"amy": 1.0, "chin": 200.0}, {"nice": 3.0, "amy": 1.0}]
        model.fit_transform(data)
        model_onnx = convert_sklearn(
            model,
            "dictionary vectorizer",
            [(
                "input",
                DictionaryType(StringTensorType([1]), FloatTensorType([1])),
            )],
        )
        self.assertTrue(model_onnx is not None)
        dump_data_and_model(
            data,
            model,
            model_onnx,
            basename="SklearnDictVectorizer-OneOff-SkipDim1",
            allow_failure="StrictVersion(onnxruntime.__version__)"
                          " <= StrictVersion('0.1.3') or "
                          "StrictVersion(onnx.__version__)"
                          " < StrictVersion('1.3.0')",
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    def test_model_dict_vectorizer_sort_false(self):
        model = DictVectorizer(sparse=False, sort=False)
        data = [{1: 1.0, 2: 200.0}, {1: 3.0, 3: 1.0}]
        model.fit_transform(data)
        model_onnx = convert_sklearn(
            model,
            "dictionary vectorizer",
            [(
                "input",
                DictionaryType(Int64TensorType([1]), FloatTensorType([1])),
            )],
        )
        self.assertTrue(model_onnx is not None)
        dump_data_and_model(
            data,
            model,
            model_onnx,
            basename="SklearnDictVectorizerSortFalse-OneOff-SkipDim1",
            allow_failure="StrictVersion(onnxruntime.__version__)"
                          " <= StrictVersion('0.1.3') or "
                          "StrictVersion(onnx.__version__)"
                          " < StrictVersion('1.3.0')",
        )


if __name__ == "__main__":
    unittest.main()
