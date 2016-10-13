import sys
import argparse
from __init__ import __version__ as ipwbVersion

# ipwb modules
import replay
import indexer
import util

IP = '127.0.0.1'
PORT = '5001'


def main():
    args = checkArgs(sys.argv)


def checkArgs_index(args):
    # print "TODO: start indexing file at path: " + args.warcPath
    if not util.isDaemonAlive():
        sys.exit()
    indexer.indexFileAt(args.warcPath)


def checkArgs_replay(args):
    # TODO: add any other sub-arguments for replay here
    replay.main()


def checkArgs(argsIn):
    """
    Check to ensure valid arguments were passed in and provides guidance
    on the available options if not
    """
    parser = argparse.ArgumentParser(
        description='InterPlanetary Wayback (ipwb)', prog="ipwb")
    subparsers = parser.add_subparsers(title="ipwb commands",
        description="Invoke using \"ipwb <command>\", e.g., ipwb replay")

    indexParser = subparsers.add_parser('index',
        prog="ipwb",
        description="Index a WARC file for replay in ipwb",
        help="Index a WARC file for replay in ipwb")
    indexParser.add_argument('warcPath',
        help="Path to a WARC[.gz] file",
        metavar="index <warcPath>",
        default=None)
    indexParser.set_defaults(func=checkArgs_index)
    replayParser = subparsers.add_parser('replay',
        prog="ipwb replay",
        help="Start the ipwb replay system")
    replayParser.set_defaults(func=checkArgs_replay)

    parser.add_argument(
      '-d', '--daemon',
      help='Location of ipfs daemon (default 127.0.0.1:5001)',
      default=IP+':'+PORT, dest='daemon_address')
    parser.add_argument('-o', '--outfile',
        help='Filename of newly created CDXJ index file')
    parser.add_argument(
      '-v', '--version', help='Report the version of ipwb', action='version',
      version='InterPlanetary Wayback ' + ipwbVersion)

    # parser.add_argument('replay',
    #   help="Index a WARC file", default=None, nargs='?')
    # parser.add_argument('--index', help="Index a WARC file",
    #  default=None, nargs=1)
    # parser.add_argument('warcPath', help="Path to a WARC[.gz] file")
    results = parser.parse_args()
    results.func(results)

    return results


if __name__ == "__main__":
    main()
