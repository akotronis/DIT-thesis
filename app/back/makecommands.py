import argparse
import subprocess

DEFAULT_BACKEND_PORT = 8000

commands = {
    'runserver':'drs() {{\n\tlocal port=${{1:-{port}}}\n\tpython manage.py runserver 0:$port\n}}',
    'shell':'dsh() {\n\tpython manage.py shell "$@"\n}',
    'makemigrations':'dmm() {\n\tpython manage.py makemigrations "$@"\n}',
    'migrate':'dmg() {\n\tpython manage.py migrate "$@"\n}',
    'showmigrations':'dsm() {\n\tpython manage.py showmigrations "$@"\n}',
}


def add_commands(args):
    container, port = args.container, args.port
    commands['runserver'] = commands['runserver'].format(port=port)
    commands_string = '\n'.join(commands.values()).replace('$', '\\$').replace('"', '\\"')
    try:
        subprocess.run(
            ["docker", "exec", "-it", container, "bash", "-c", f"echo \"{commands_string}\" > $HOME/.bashrc"],
            check=True
        )
        print(f'String successfully added to ~/.bashrc of {container}')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred: {e}')


def parse_command():
    """
    Parse CLI input to create django manage command shortcuts to
    web container's ~/.bashrc file.
    - Run `>>> python -m makecommands --h` for help
    - Pass container name (-c) to send there the commands
    - Pass port (-p) for default python manage.py runserver command port
    """
    parser = argparse.ArgumentParser('Put django commands in container')
    parser.add_argument(
        '-c', '--container',
        type=str,
        required=True,
        help='Container name to the ~/.bashrc of which to put the commands.'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=DEFAULT_BACKEND_PORT,
        help='Port for runserver command'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command()
    add_commands(args)