import argparse

from py2zenodo import Deposition


def parse_args():
    parser = argparse.ArgumentParser(
        description="Python wrapper for Zenodo REST API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-f", "--files", nargs="+", help="Files to upload.")
    parser.add_argument("-t", "--token", required=True, help="Access token.")
    parser.add_argument("-s", "--sandbox", action="store_true", help="Use sandbox.")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    depo = Deposition(access_token=args.token, sandbox=args.sandbox)
    depo.create_new_depo(verbose=args.verbose)
    for file in args.files:
        depo.upload_file(file)
