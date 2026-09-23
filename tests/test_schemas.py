import pytest
from pydantic import ValidationError

from app.schemas import EvaluationRequest, EvaluationResult


def test_average_is_mean_of_accuracy_and_tone():
    result = EvaluationResult(
        accuracy_score=4, tone_score=2, errors=[], verdict="PASS", average_score=3.0
    )
    assert result.average == 3.0


@pytest.mark.parametrize(
    "raw_verdict, expected",
    [
        ("pass", "PASS"),
        ("Pass", "PASS"),
        (" PASS ", "PASS"),
        ("fail", "FAIL"),
    ],
)
def test_verdict_is_normalized_to_upper_without_spaces(raw_verdict, expected):
    result = EvaluationResult(
        accuracy_score=5, tone_score=5, errors=[], verdict=raw_verdict, average_score=5.0
    )
    assert result.verdict == expected


def test_invalid_verdict_raises_validation_error():
    with pytest.raises(ValidationError):
        EvaluationResult(
            accuracy_score=5, tone_score=5, errors=[], verdict="MAYBE", average_score=5.0
        )


@pytest.mark.parametrize("bad_score", [0, 6, -1])
def test_accuracy_score_outside_1_to_5_raises(bad_score):
    with pytest.raises(ValidationError):
        EvaluationResult(
            accuracy_score=bad_score, tone_score=5, errors=[], verdict="PASS", average_score=5.0
        )


def test_errors_defaults_to_empty_list():
    result = EvaluationResult(
        accuracy_score=5, tone_score=5, verdict="PASS", average_score=5.0
    )
    assert result.errors == []


def test_reference_context_is_optional():
    request = EvaluationRequest(user_query="q", bot_response="a")
    assert request.reference_context is None
