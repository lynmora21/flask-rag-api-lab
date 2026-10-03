MIN_QUESTION_LENGTH = 3


def validate_question_payload(payload):
    """Validate the JSON body for POST /api/ask.

    Return:
        (question, None) when valid
        (None, error_dict) when invalid
    """
    if not isinstance(payload, dict):
        return None, {
            "error": "invalid_request",
            "message": "Request body must be a JSON object.",
        }

    if "question" not in payload:
        return None, {
            "error": "missing_question",
            "message": "Question is required.",
        }

    question = payload["question"]

    if not isinstance(question, str):
        return None, {
            "error": "invalid_question",
            "message": "Question must be a string.",
        }

    question = question.strip()

    if not question:
        return None, {
            "error": "empty_question",
            "message": "Question cannot be blank.",
        }

    if len(question) < MIN_QUESTION_LENGTH:
        return None, {
            "error": "short_question",
            "message": "Question must be at least 3 characters long.",
        }

    return question, None
