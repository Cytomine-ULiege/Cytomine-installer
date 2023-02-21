from argparse import ArgumentParser
from os import getcwd
import os

from bootstrapper.actions.util import prompt_proceed_question

from ..deployment.deployment_folders import DeploymentFolder
from bootstrapper.actions.base import AbstractAction


class CleanAction(AbstractAction):
    def _fill_in_subparser(self, sub_parser: ArgumentParser):
        """Fill the given sub_parser with the program arguments"""
        sub_parser.description = "clean files generated by the bootstrapper that might be present in the 'target_directory' (using 'working_directory' as a reference)"
        sub_parser.add_argument(
            "-w",
            "--working_directory",
            dest="working_directory",
            help="path to the working directory",
            default=getcwd(),
        )
        sub_parser.add_argument(
            "-t",
            "--target_directory",
            dest="target_directory",
            help="path to target directory to clean",
            default=getcwd(),
        )
        sub_parser.add_argument(
            "--env-folder-name",
            dest="env_folder_name",
            help="name of the environment variables folder",
            default="envs",
        )
        sub_parser.add_argument(
            "--config-folder-name",
            dest="config_folder_name",
            help="name of the configs folder",
            default="configs",
        )
        sub_parser.add_argument(
            "-i",
            "--ignored",
            dest="ignored_dirs",
            help="folders to ignores in working directory",
        )

    def run(self, namespace):
        """Executes the actions.
        Parameters
        ----------
        namespace: Namespace
          Command line arguments of the action (including local/global scope information)
        """
        if namespace.ignored_dirs is None:
            namespace.ignored_dirs = []
        deployment = DeploymentFolder(
            directory=namespace.working_directory,
            ignored_dirs=namespace.ignored_dirs,
            envs_folder=namespace.envs_folder_name,
            configs_folder=namespace.configs_folder_name,
        )

        if os.path.normpath(namespace.working_directory) == os.path.normpath(
            namespace.target_directory
        ):
            prompt_proceed_question("clean: working and target directory are the same")

        self.get_logger().info(f"cleaning '{namespace.working_directory}''")
        deployment.clean_generated_files(namespace.target_directory)
