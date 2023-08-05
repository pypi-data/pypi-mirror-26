"""Methods to verify previously created pacts."""
import sys
from os.path import isfile

import click

from .constants import VERIFIER_PATH

if sys.version_info.major == 2:
    import subprocess32 as subprocess
else:
    import subprocess


@click.command()
@click.option(
    'base_url', '--provider-base-url',
    help='Base URL of the provider to verify against.',
    required=True)
@click.option(
    'pact_url', '--pact-url',
    help='The URI of the pact to verify.'
         ' Can be an HTTP URI or a local file path.'
         ' It can be specified multiple times to verify several pacts.',
    multiple=True)
@click.option(
    'pact_urls', '--pact-urls',
    default='',
    help='The URI(s) of the pact to verify.'
         ' Can be an HTTP URI(s) or local file path(s).'
         ' Provide multiple URI separated by a comma.',
    multiple=True)  # Remove in major version 1.0.0
@click.option(
    'states_url', '--provider-states-url',
    help='DEPRECATED: URL to fetch the provider states for'
         ' the given provider API.')  # Remove in major version 1.0.0
@click.option(
    'states_setup_url', '--provider-states-setup-url',
    help='URL to send PUT requests to setup a given provider state.')
@click.option(
    'username', '--pact-broker-username',
    help='Username for Pact Broker basic authentication.')
@click.option(
    'password', '--pact-broker-password',
    envvar='PACT_BROKER_PASSWORD',
    help='Password for Pact Broker basic authentication. Can also be specified'
         ' via the environment variable PACT_BROKER_PASSWORD')
@click.option(
    'timeout', '-t', '--timeout',
    default=30,
    help='The duration in seconds we should wait to confirm verification'
         ' process was successful. Defaults to 30.',
    type=int)
def main(base_url, pact_url, pact_urls, states_url, states_setup_url, username,
         password, timeout):
    """
    Verify one or more contracts against a provider service.

    Minimal example:

        pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pact
    """  # NOQA
    error = click.style('Error:', fg='red')
    warning = click.style('Warning:', fg='yellow')
    all_pact_urls = list(pact_url)
    for urls in pact_urls:  # Remove in major version 1.0.0
        all_pact_urls.extend(p for p in urls.split(',') if p)

    if len(pact_urls) > 1:
        click.echo(
            warning
            + ' Multiple --pact-urls arguments are deprecated. '
              'Please provide a comma separated list of pacts to --pact-urls, '
              'or multiple --pact-url arguments.')

    if not all_pact_urls:
        click.echo(
            error
            + ' At least one of --pact-url or --pact-urls is required.')
        raise click.Abort()

    missing_files = [path for path in all_pact_urls if not path_exists(path)]
    if missing_files:
        click.echo(
            error
            + ' The following Pact files could not be found:\n'
            + '\n'.join(missing_files))
        raise click.Abort()

    options = {
        '--provider-base-url': base_url,
        '--pact-urls': ','.join(all_pact_urls),
        '--provider-states-setup-url': states_setup_url,
        '--broker-username': username,
        '--broker-password': password
    }

    command = [VERIFIER_PATH] + [
        '{}={}'.format(k, v) for k, v in options.items() if v]

    p = subprocess.Popen(command)
    p.communicate(timeout=timeout)
    sys.exit(p.returncode)


def path_exists(path):
    """
    Determine if a particular path exists.

    Can be provided a URL or local path. URLs always result in a True. Local
    paths are True only if a file exists at that location.

    :param path: The path to check.
    :type path: str
    :return: True if the path exists and is a file, otherwise False.
    :rtype: bool
    """
    if path.startswith('http://') or path.startswith('https://'):
        return True

    return isfile(path)


if __name__ == '__main__':
    sys.exit(main())
