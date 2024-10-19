import unittest
from unittest.mock import Mock

from vedro_pairwise import ParamsPairwise, params_pairwise


class TestParamsPairwise(unittest.TestCase):

    def _to_params(self, args):
        return (args, {}, ())

    def _get_params(self, fn):
        return getattr(fn, "__vedro__params__")

    def test_instance_creation(self):
        matrix = params_pairwise(["chrome", "firefox"])
        self.assertIsInstance(matrix, ParamsPairwise)

    def test_empty_params(self):
        matrix = params_pairwise()
        mock = Mock()

        with self.assertRaises(ValueError):
            matrix(mock)

    def test_combinations_of_three_params(self):
        matrix = params_pairwise(["x1", "x2"], ["y1", "y2"], ["z1", "z2"])
        mock = Mock()

        res = matrix(mock)

        self.assertEqual(res, mock)
        self.assertEqual(mock.mock_calls, [])
        self.assertEqual(self._get_params(mock), [
            self._to_params(("x1", "y2", "z2")),
            self._to_params(("x2", "y1", "z2")),
            self._to_params(("x2", "y2", "z1")),
            self._to_params(("x1", "y1", "z1")),
        ])

    def test_combinations_with_keyword_args(self):
        matrix = params_pairwise(x=["x1", "x2"], y=["y1", "y2"])
        mock = Mock()

        res = matrix(mock)

        self.assertEqual(res, mock)
        self.assertEqual(mock.mock_calls, [])
        self.assertEqual(self._get_params(mock), [
            self._to_params(("x1", "y2")),
            self._to_params(("x2", "y2")),
            self._to_params(("x2", "y1")),
            self._to_params(("x1", "y1")),
        ])

    def test_combinations_with_mixed_args(self):
        matrix = params_pairwise(["x1", "x2"], y=["y1", "y2"])
        mock = Mock()

        res = matrix(mock)

        self.assertEqual(res, mock)
        self.assertEqual(mock.mock_calls, [])
        self.assertEqual(self._get_params(mock), [
            self._to_params(("x1", "y2")),
            self._to_params(("x2", "y2")),
            self._to_params(("x2", "y1")),
            self._to_params(("x1", "y1")),
        ])


if __name__ == "__main__":
    unittest.main()
