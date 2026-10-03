from flask import Flask, jsonify, request

from lib.model_client import ModelClientError
from lib.rag_service import answer_question
from lib.validation import validate_question_payload
from lib.response_formatter import format_error_response


def create_app():
    app = Flask(__name__)

    @app.post("/api/ask")
    def ask():
        payload = request.get_json(silent=True)

        question, error = validate_question_payload(payload)

        if error:
            return jsonify(error), 400

        try:
            result = answer_question(question)
            return jsonify(result), 200

        except ModelClientError as exc:
            return jsonify(
                format_error_response(
                    "model_service_error",
                    str(exc),
                )
            ), 502

    return app


app = create_app()
