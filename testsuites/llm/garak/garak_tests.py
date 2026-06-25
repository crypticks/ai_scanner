from .garak_generator import CustomGenerator
import argparse
import datetime

from garak import __description__
from garak import _config, _plugins
from garak.exception import GarakException
import garak.command as command
import logging
import re

def run_test_suite(comm_function, probes: list[str], parsed_specs) -> list[dict]:
    parsed_specs = {
    "probe": ["probes.lmrc.Bullying"],
    "detector": [],
    "buff": []
}

    _config.transient.starttime = datetime.datetime.now()
    _config.transient.starttime_iso = _config.transient.starttime.isoformat()
    from argparse import Namespace

    _config.transient.cli_args = Namespace(
        probes=",".join(probes),
        list_probes=False,
        list_detectors=False,
        list_generators=False,
        list_buffs=False,
        list_config=False,
        plugin_info=None,
        interactive=False,
        verbose=0
    )
    log_filename = command.start_logging()
    _config.load_base_config()

    print(
        f"garak {__description__} v{_config.version} ( https://github.com/NVIDIA/garak ) at {_config.transient.starttime_iso}"
    )
    # startup
    import sys
    import json

    import garak.evaluators

    try:

            print(f"📜 logging to {log_filename}")


            evaluator = garak.evaluators.ThresholdEvaluator(_config.run.eval_threshold)
            generator = CustomGenerator(comm_function)


            command.start_run()  # start the run now that all config validation is complete
            print(f"📜 reporting to {_config.transient.report_filename}")

            from garak.generators.base import Conversation, Message

            conv = Conversation.from_openai([
                {"role": "user", "content": {"text": "Hello"}}
            ])
            generator.parallel_requests = 1
            generator.parallel_capable = False

            _config.system.parallel_attempts = 1
            _config.system.parallel_requests = 1

            if parsed_specs["detector"] == []:
                command.probewise_run(
                    generator, parsed_specs["probe"], evaluator, parsed_specs["buff"]
                )
            else:
                command.pxd_run(
                    generator,
                    parsed_specs["probe"],
                    parsed_specs["detector"],
                    evaluator,
                    parsed_specs["buff"],
                )

            command.end_run()
            return []


    except KeyboardInterrupt as e:
        msg = "User cancel received, terminating all runs"
        logging.exception(e)
        logging.info(msg)
        print(msg)
    except (ValueError, GarakException) as e:
        logging.exception(e)
        print(e)
