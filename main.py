import argparse
import logging
import sys

from pipeline_class import PipelineClass
from setup_class import SetupClass
from side import Side

_log = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INVALID = 2


def main(argv=None):
    """!
    @brief Runs the dual-projector program from command-line arguments

    @param argy Command-line arguments. If None, argparse reads sys.argy

    @return Exit code 0: for normal completion, 1 if the settings or source picture cannot be read or the pipeline fails, 
    and 2 if settings are unusabel or the command-line arguments are invalid
    @rtype int

    @throws SystemExit argparse raises this for invalid command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Show this computer's half of the dual-projector picture.")
    parser.add_argument("settings", help="path to the settings JSON file")
    parser.add_argument("--side", choices=["LEFT", "RIGHT"], type=str.upper,
                        help="which projector this computer drives (overrides projectorSide "
                             "in the settings file)")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO)

    setup = SetupClass()
    try:
        setup.load(args.settings)
    except (OSError, ValueError) as e:
        _log.error("Cannot load settings: %s", e)
        return EXIT_ERROR

    if args.side:
        setup.setProjectorSide(Side[args.side])

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
