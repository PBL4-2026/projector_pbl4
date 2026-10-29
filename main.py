import argparse
import logging
import sys

from pipeline_class import PipelineClass
from setup_class import SetupClass

_log = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INVALID = 2


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Show this computer's half of the dual-projector picture.")
    parser.add_argument("settings", help="path to the settings JSON file")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO)

    setup = SetupClass()
    try:
        setup.load(args.settings)
    except (OSError, ValueError) as e:
        _log.error("Cannot load settings: %s", e)
        return EXIT_ERROR

    if not setup.validate():
        return EXIT_INVALID

    try:
        PipelineClass(setup).run()
    except (OSError, ValueError) as e:
        _log.error("Cannot run: %s", e)
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
