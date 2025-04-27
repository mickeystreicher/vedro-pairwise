from unittest.mock import Mock

from vedro import catched
from vedro_fn import given, scenario, then, when

from vedro_pairwise import ParamsPairwise, params_pairwise


@scenario()
def create_params_pairwise():
    with given:
        matrix = None

    with when:
        matrix = params_pairwise(["chrome", "firefox"])

    with then:
        assert isinstance(matrix, ParamsPairwise)


@scenario()
def try_to_create_pairwise_with_empty_params():
    with given:
        matrix = params_pairwise()
        mock = Mock()

    with when, catched(Exception) as exc_info:
        matrix(mock)

    with then:
        assert exc_info.type is ValueError


@scenario()
def generate_pairwise_combinations_of_three_params():
    with given:
        mock = Mock()
        matrix = params_pairwise(["x1", "x2"], ["y1", "y2"], ["z1", "z2"])

    with when:
        res = matrix(mock)

    with then:
        assert res == mock
        assert mock.mock_calls == []
        assert getattr(mock, "__vedro__params__") == [
            (("x1", "y2", "z2"), {}, ()),
            (("x2", "y1", "z2"), {}, ()),
            (("x2", "y2", "z1"), {}, ()),
            (("x1", "y1", "z1"), {}, ()),
        ]


@scenario()
def generate_pairwise_combinations_with_keyword_args():
    with given:
        mock = Mock()
        matrix = params_pairwise(x=["x1", "x2"], y=["y1", "y2"])

    with when:
        res = matrix(mock)

    with then:
        assert res == mock
        assert mock.mock_calls == []
        assert getattr(mock, "__vedro__params__") == [
            (("x1", "y2"), {}, ()),
            (("x2", "y2"), {}, ()),
            (("x2", "y1"), {}, ()),
            (("x1", "y1"), {}, ()),
        ]


@scenario()
def generate_pairwise_combinations_with_mixed_args():
    with given:
        mock = Mock()
        matrix = params_pairwise(["x1", "x2"], y=["y1", "y2"])

    with when:
        res = matrix(mock)

    with then:
        assert res == mock
        assert mock.mock_calls == []
        assert getattr(mock, "__vedro__params__") == [
            (("x1", "y2"), {}, ()),
            (("x2", "y2"), {}, ()),
            (("x2", "y1"), {}, ()),
            (("x1", "y1"), {}, ()),
        ]
