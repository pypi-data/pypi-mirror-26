import os

import click
from pluginbase import PluginBase

from .credentials import load_credentials
from .utils.artifactory import Artifactory
from .utils.logging import getLogger
from .utils.performance import get_performance_report
from .exceptions import InvalidPoliciesDirectory

LOG = getLogger(__name__)


@click.command()
@click.option(
    '--dryrun/--nodryrun', default=True, is_flag=True, help='Dryrun does not delete any artifacts. On by default')
@click.option('--default/--no-default', default=True, is_flag=True, help='If false, does not apply default policy')
@click.option('--policies-path', required=False, help='Path to extra policies directory')
#@click.argument('url')
def purge(dryrun, policies_path, default):  #, url):
    credentials = load_credentials()
    artifactory = Artifactory(credentials['artifactory_url'], credentials['artifactory_username'],
                              credentials['artifactory_password'])

    plugin_source = setup_pluginbase(extra_policies_path=policies_path)
    before = artifactory.list(None)
    for repo, info in before.items():
        policy_name = repo.replace("-", "_")
        try:
            policy = plugin_source.load_plugin(policy_name)
        except ModuleNotFoundError:
            if default:
                LOG.info("No policy found for %s. Applying Default", repo)
                policy = plugin_source.load_plugin('default')
            else:
                LOG.info("No policy found for %s. Skipping Default", repo)
                continue
        artifacts = policy.purgelist(
            artifactory,
            repo,
            None,
        )
        count = artifactory.purge(repo, dryrun, artifacts)
        LOG.info("Processed {}, Purged {}".format(repo, count))

    LOG.info("")
    LOG.info("Purging Performance:")
    after = artifactory.list(None)
    for repo, info in after.items():
        try:
            get_performance_report(repo, before[repo], info)
        except IndexError:
            pass

    LOG.info("Done.")

    exit(0)


def setup_pluginbase(extra_policies_path=None):
    """Sets up plugin base with default path and provided path

    Args:
        extra_policies_path (str): Extra path to find plugins in

    Returns:
        PluginSource: PluginBase PluginSource for finding plugins
    """
    here = os.path.dirname(os.path.realpath(__file__))
    default_path = "{}/policies".format(here)
    all_paths = [default_path]
    if extra_policies_path:
        if not os.path.isdir(extra_policies_path):
            raise InvalidPoliciesDirectory
        all_paths.append(extra_policies_path)
    LOG.info("Searching for policies in %s", str(all_paths))
    plugin_base = PluginBase(package='lavatory.policy_plugins')
    plugin_source = plugin_base.make_plugin_source(searchpath=all_paths)
    LOG.debug("Policies found: %s", str(plugin_source.list_plugins()))
    return plugin_source


if __name__ == "__main__":
    purge()
