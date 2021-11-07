import os
import tempfile
from subprocess import call

# Get the EDITOR or default to vim
EDITOR = os.environ.get("EDITOR", "vim")

# Used to create a file by writting to it
initial_message = b""

# Open a temporary file
with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    # Create the file
    tf.write(initial_message)
    tf.flush()

    # Open the file in the EDITOR
    call([EDITOR, tf.name])

    # Get the file contents
    tf.seek(0)
    edited_message = tf.read()

# Decode and print out to it
print(edited_message.decode("utf-8"))
