import cmd
import os
import shlex
import tempfile
from subprocess import call

EDITOR = os.environ.get("EDITOR", "vim")


class Shell(cmd.Cmd):
    intro = "Additional field shell."
    prompt = "\\ >_< / .: "
    file = None

    # ----- basic turtle commands -----
    def do_head(self, arg):
        """Open the EDITOR and get the contents from it"""
        header = shlex.split(arg)
        value = get_value_from_editor()
        print(header)
        print(value)

    def do_exit(self, arg):
        """Exit the shell"""
        return True


def launch_shell():
    Shell().cmdloop()


def get_value_from_editor(initial_message=b"") -> str:
    """Open the editor and get the written contents"""
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        open_editor(tf.name)
        return tf.read().decode("utf-8").rstrip()


def open_editor(filename):
    """Opens the EDITOR"""
    call([EDITOR, filename])


if __name__ == "__main__":
    launch_shell()
