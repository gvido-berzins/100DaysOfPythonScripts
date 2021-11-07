import os
import tempfile
from subprocess import call

# Get the EDITOR or default to vim
EDITOR = os.environ.get("EDITOR", "vim")


def editor() -> str:
    """Open the editor and get the written contents"""
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(b"")
        call([EDITOR, tf.name])
        return tf.read().decode("utf-8").rstrip()


message = editor()
print(message)
