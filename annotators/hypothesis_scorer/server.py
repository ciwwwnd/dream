import logging
import os
import time

import sentry_sdk
import uvicorn as uvicorn
from catboost import CatBoostClassifier
from fastapi import FastAPI
from pydantic import BaseModel, conlist
from sentry_sdk.integrations.logging import ignore_logger

from annotators.hypothesis_scorer import test_server
from score import get_features

ignore_logger("root")

sentry_sdk.init(os.getenv("SENTRY_DSN"))
SERVICE_NAME = os.getenv("SERVICE_NAME")
SERVICE_PORT = int(os.getenv("SERVICE_PORT"))
RANDOM_SEED = int(os.getenv("RANDOM_SEED", 2718))

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("werkzeug").setLevel("WARNING")

app: FastAPI = FastAPI()


def get_probas(contexts, hypotheses):
    features = get_features(contexts, hypotheses)
    pred = cb.predict_proba(features)[:, 1]
    return pred


try:
    cb = CatBoostClassifier()
    cb.load_model("model-confidence-convert-old_midas.cbm")
    contexts = [
        [
            "i'm good how are you",
            "Spectacular, by all reports! Do you want to know what I can do?",
            "absolutely",
            "I'm a socialbot running inside Alexa, and I'm all about chatting with people like you. "
            "I can answer questions, share fun facts, discuss movies, books and news. What do you want to talk about?",
            "let's talk about movies",
        ]
    ]
    hypotheses = [
        {
            "is_best": True,
            "text": "Kong: Skull Island is a good action movie. What do you think about it?",
            "confidence": 1.0,
            "cobot_convers_evaluator_annotator": {
                "isResponseOnTopic": 0.505,
                "isResponseErroneous": 0.938,
                "responseEngagesUser": 0.344,
                "isResponseInteresting": 0.084,
                "isResponseComprehensible": 0.454,
            },
        }
    ]
    get_probas(contexts, hypotheses)
except Exception as e:
    logger.exception("Scorer not loaded")
    sentry_sdk.capture_exception(e)
    raise e


def handler(contexts, hypotheses):
    st_time = time.time()

    try:
        responses = get_probas(contexts, hypotheses).tolist()
    except Exception as e:
        responses = [0] * len(hypotheses)
        sentry_sdk.capture_exception(e)
        logger.exception(e)

    logging.warning(f"hypothesis_scorer exec time {time.time() - st_time}")
    return [{"batch": responses}]


try:
    test_server.main_test()  # TODO: Rewrite tests!!!!
    logger.info("test query processed")
except Exception as exc:
    sentry_sdk.capture_exception(exc)
    logger.exception(exc)
    raise exc

logger.info(f"{SERVICE_NAME} is loaded and ready")


class HypothesesSchema(BaseModel):
    is_best: bool
    text: str
    confidence: float


class RequestSchema(BaseModel):
    contexts: conlist(item_type=conlist(item_type=str, min_items=0), min_items=0)
    hypotheses: conlist(item_type=HypothesesSchema, min_items=0)


@app.post("/batch_model")
async def batch_respond(request: RequestSchema):
    return handler(request.contexts, request.hypotheses)


if __name__ == "__main__":
    uvicorn.run(app, debug=False, host="0.0.0.0", port=3000)
