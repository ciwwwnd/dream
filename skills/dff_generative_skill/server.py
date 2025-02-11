#!/usr/bin/env python

import logging
import time
import os
import random
import requests

import sentry_sdk
from flask import Flask, request, jsonify
from healthcheck import HealthCheck
from sentry_sdk.integrations.logging import ignore_logger

from common.dff.integration.actor import load_ctxs, get_response
from scenario.main import actor

import test_server


ignore_logger("root")

sentry_sdk.init(os.getenv("SENTRY_DSN"))
SERVICE_NAME = os.getenv("SERVICE_NAME")
SERVICE_PORT = int(os.getenv("SERVICE_PORT"))
RANDOM_SEED = int(os.getenv("RANDOM_SEED", 2718))
DIALOGPT_SERVICE_URL = os.environ["DIALOGPT_SERVICE_URL"]

logging.basicConfig(format="%(asctime)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)
health = HealthCheck(app, "/healthcheck")
logging.getLogger("werkzeug").setLevel("WARNING")


def is_container_running():
    try:
        requested_data = [{"speaker": "human", "text": "привет"}]
        response = requests.post(DIALOGPT_SERVICE_URL, json={"dialog_contexts": [requested_data]}, timeout=4)
        if response.status_code == 200:
            return True
    except Exception as exc:
        print(exc)
        return False
    return False


def handler(requested_data, random_seed=None):
    st_time = time.time()
    ctxs = load_ctxs(requested_data)
    random_seed = requested_data.get("random_seed", random_seed)  # for tests

    responses = []
    for ctx in ctxs:
        try:
            # for tests
            if random_seed:
                random.seed(int(random_seed))
            ctx = actor(ctx)
            responses.append(get_response(ctx, actor))
        except Exception as exc:
            sentry_sdk.capture_exception(exc)
            logger.exception(exc)
            responses.append(("", 0.0, {}, {}, {}))

    total_time = time.time() - st_time
    logger.info(f"{SERVICE_NAME} exec time = {total_time:.3f}s")
    return responses


while True:
    result = is_container_running()
    if result:
        break
    else:
        time.sleep(5)
        continue

try:
    test_server.run_test(handler)
    logger.info("test query processed")
except Exception as exc:
    sentry_sdk.capture_exception(exc)
    logger.exception(exc)
    raise exc


logger.info(f"{SERVICE_NAME} is loaded and ready")

# import pathlib
# import json

# for in_file in pathlib.Path("tests").glob("./*_in.json"):
#     logger.error(in_file)
#     test_in = json.load(in_file.open())
#     responses = handler(test_in, RANDOM_SEED)
#     out_file = str(in_file).replace("in.json", "out.json")
#     import common.test_utils as t_utils

#     t_utils.save_to_test(responses, out_file, indent=4)  # TEST


@app.route("/respond", methods=["POST"])
def respond():
    # import common.test_utils as t_utils; t_utils.save_to_test(request.json,"tests/lets_talk_in.json",indent=4)  # TEST
    # responses = handler(request.json, RANDOM_SEED)  # TEST
    # import common.test_utils as t_utils; t_utils.save_to_test(responses,"tests/lets_talk_out.json",indent=4)  # TEST
    responses = handler(request.json)
    return jsonify(responses)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=SERVICE_PORT)
