import subprocess
from . import testUtil as ipwb_test


def test_piping():
    new_warc_path = ipwb_test.createUniqueWARC()
    indexer_process = subprocess.Popen(["ipwb", "index", new_warc_path],
                                       stdout=subprocess.PIPE)
    replay_process = subprocess.Popen(["ipwb", "replay"], stdin=p1.stdout)
    indexer_process.stdout.close()
    replay_process.communicate()
