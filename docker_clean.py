import click
import subprocess
import sys


@click.group(help="Command to clean unused docker images, containers, etc ...")
@click.version_option('0.1')
def clean():
    pass


@clean.command(help="Restart the servers")
@click.option('--force', help="Do it", is_flag=True)
@click.option('--verbose', help="Display more information about what is removed", is_flag=True)
def main(force: bool, verbose: bool):
    print(click.style('Clean Docker stopped containers, images, volumes and networks', fg='green'))

    remove_containers(force, verbose)
    print()
    remove_images(force, verbose)
    print()
    remove_volumes(force, verbose)
    print()
    remove_networks(force, verbose)

    if force is False:
        print(click.style("\n--force is not set so I won't do anything", fg='red'))

    print(click.style('\nDone', fg='green'))


def remove_containers(force: bool, verbose: bool):
    cmd = ['docker', 'ps', '--no-trunc', '-a', '-q', '-f', 'status=exited']
    containers = subprocess.check_output(cmd, stderr=subprocess.STDOUT).splitlines()

    if len(containers) == 0:
        print('No exited container to remove')
        return

    print('Removing {} exited container(s)'.format(len(containers)))

    for container in containers:
        container = container.decode("utf-8", "strict")
        if verbose is True:
            cmd = ['docker', 'inspect', '--format={{.Name}}', container]
            container_name = subprocess.check_output(cmd, stderr=subprocess.STDOUT).splitlines()[0]

            print('  Removing container {}'.format(container_name.decode("utf-8", "strict")))

        if force is True:
            subprocess.check_output(['docker', 'rm', container])


def remove_images(force: bool, verbose: bool):
    cmd = ['docker', 'images', '--no-trunc', '-q', '-f', 'dangling=true']
    images = subprocess.check_output(cmd, stderr=subprocess.STDOUT).splitlines()

    if len(images) == 0:
        print('No image to remove')
        return

    print('Removing {} dangling image(s)'.format(len(images)))

    for image in images:
        image = image.decode("utf-8", "strict")
        if verbose is True:
            print('  Removing image {}'.format(image))

        if force is True:
            subprocess.check_output(['docker', 'rmi', image])


def remove_volumes(force: bool, verbose: bool):
    cmd = ['docker', 'volume', 'ls', '-q', '-f', 'dangling=true']
    volumes = subprocess.check_output(cmd, stderr=subprocess.STDOUT).splitlines()

    if len(volumes) == 0:
        print('No volume to remove')
        return

    print('Removing {} exited volumes(s)'.format(len(volumes)))

    for volume in volumes:
        volume = volume.decode("utf-8", "strict")
        if verbose is True:
            print('  Removing volume {}'.format(volume))

        if force is True:
            subprocess.check_output(['docker', 'volume', 'rm', volume])


def remove_networks(force: bool, verbose: bool):
    cmd = ['docker', 'network', 'ls', '--no-trunc', '-q', '--filter', 'type=custom']
    networks = subprocess.check_output(cmd, stderr=subprocess.STDOUT).splitlines()

    if len(networks) == 0:
        print('No network to remove')
        return

    print('Removing {} exited networks(s)'.format(len(networks)))

    for network in networks:
        network = network.decode("utf-8", "strict")
        if verbose is True:
            cmd = ['docker', 'network', 'inspect', '--format={{.Name}}', network]
            network_name = subprocess.check_output(cmd, stderr=subprocess.STDOUT).splitlines()[0]
            print('  Removing network {}'.format(network_name.decode("utf-8", "strict")))

        if force is True:
            subprocess.check_output(['docker', 'network', 'rm', network])


if __name__ == '__main__':
    try:
        clean()
    except Exception as e:
        msg = click.style(r""" ______ _____  _____   ____  _____
|  ____|  __ \|  __ \ / __ \|  __ \
| |__  | |__) | |__) | |  | | |__) |
|  __| |  _  /|  _  /| |  | |  _  /
| |____| | \ \| | \ \| |__| | | \ \
|______|_|  \_\_|  \_\\____/|_|  \_\

""", fg='yellow')
        msg += click.style('{}'.format(e), fg='red')

        print(msg)
        print("")
        # raise e
        sys.exit(1)