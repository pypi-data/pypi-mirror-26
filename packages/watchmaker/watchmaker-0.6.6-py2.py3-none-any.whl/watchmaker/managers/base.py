# -*- coding: utf-8 -*-
"""Watchmaker base manager."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import abc
import concurrent.futures
import logging
import os
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

from six import add_metaclass
from six.moves import urllib

from watchmaker.exceptions import WatchmakerException


class ManagerBase(object):
    """
    Base class for operating system managers.

    All child classes will have access to methods unless overridden by an
    identically-named method in the child class.

    Args:
        system_params: (:obj:`dict`)
            Attributes, mostly file-paths, specific to the system-type (Linux
            or Windows). The dict keys are as follows:

            prepdir:
                Directory where Watchmaker will keep files on the system.
            readyfile:
                Path to a file that will be created upon successful
                completion.
            logdir:
                Directory to store log files.
            workingdir:
                Directory to store temporary files. Deleted upon successful
                completion.
            restart:
                Command to use to restart the system upon successful
                completion.
            shutdown_path:
                (Windows-only) Path to the Windows ``shutdown.exe`` command.

    """

    boto3 = None
    boto_client = None

    def __init__(self, system_params, *args, **kwargs):
        self.log = logging.getLogger(
            '{0}.{1}'.format(__name__, self.__class__.__name__)
        )
        self.system_params = system_params
        self.working_dir = None
        args = args
        kwargs = kwargs

    def _import_boto3(self):
        if self.boto3:
            return

        self.log.info("Dynamically importing boto3 ...")
        try:
            self.boto3 = __import__("boto3")
            self.boto_client = __import__(
                "botocore.client",
                globals(),
                locals(),
                ["ClientError"],
                0
            )
        except ImportError:
            msg = 'Unable to import boto3 module.'
            self.log.critical(msg)
            raise

    def _get_s3_file(self, url, bucket_name, key_name, destination):
        self._import_boto3()

        try:
            s3_ = self.boto3.resource("s3")
            s3_.meta.client.head_bucket(Bucket=bucket_name)
            s3_.Object(bucket_name, key_name).download_file(destination)
        except self.boto_client.ClientError:
            msg = 'Bucket does not exist.  bucket = {0}.'.format(bucket_name)
            self.log.critical(msg)
            raise
        except Exception:
            msg = (
                'Unable to download file from S3 bucket. url = {0}. '
                'bucket = {1}. key = {2}. file = {3}.'
                .format(url, bucket_name, key_name, destination)
            )
            self.log.critical(msg)
            raise

    def download_file(self, url, filename, sourceiss3bucket=False):
        """
        Download a file from a web server or S3 bucket.

        Args:
            url: (:obj:`str`)
                URL to a file.

            filename: (:obj:`str`)
                Path where the file will be saved.

            sourceiss3bucket: (:obj:`bool`)
                Switch to indicate that the download should use boto3 to
                download the file from an S3 bucket.
                (*Default*: ``False``)
        """
        self.log.debug('Downloading: %s', url)
        self.log.debug('Destination: %s', filename)
        self.log.debug('S3: %s', sourceiss3bucket)

        if sourceiss3bucket:
            self._import_boto3()

            bucket_name = url.split('/')[3]
            key_name = '/'.join(url.split('/')[4:])

            self.log.debug('Bucket Name: %s', bucket_name)
            self.log.debug('key_name: %s', key_name)

            try:
                s3_ = self.boto3.resource('s3')
                s3_.meta.client.head_bucket(Bucket=bucket_name)
                s3_.Object(bucket_name, key_name).download_file(filename)
            except (NameError, self.boto_client.ClientError):
                self.log.error('NameError: %s', self.boto_client.ClientError)
                try:
                    bucket_name = url.split('/')[2].split('.')[0]
                    key_name = '/'.join(url.split('/')[3:])
                    s3_ = self.boto3.resource("s3")
                    s3_.meta.client.head_bucket(Bucket=bucket_name)
                    s3_.Object(bucket_name, key_name).download_file(filename)
                except Exception:
                    msg = (
                        'Unable to download file from S3 bucket. url = {0}. '
                        'bucket = {1}. key = {2}. file = {3}.'
                        .format(url, bucket_name, key_name, filename)
                    )
                    self.log.critical(msg)
                    raise
            except Exception:
                msg = (
                    'Unable to download file from S3 bucket. url = {0}. '
                    'bucket = {1}. key = {2}. file = {3}.'
                    .format(url, bucket_name, key_name, filename)
                )
                self.log.critical(msg)
                raise
            self.log.info(
                'Downloaded file from S3 bucket. url=%s. filename=%s',
                url, filename
            )
        else:
            try:
                self.log.debug('Opening connection to web server, %s', url)
                response = urllib.request.urlopen(url)
                self.log.debug('Opening the file handle, %s', filename)
                with open(filename, 'wb') as outfile:
                    self.log.debug('Saving file to local filesystem...')
                    shutil.copyfileobj(response, outfile)
            except Exception:
                msg = (
                    'Unable to download file from web server. url = {0}. '
                    'filename = {1}.'
                    .format(url, filename)
                )
                self.log.critical(msg)
                raise
            self.log.info(
                'Downloaded file from web server. url=%s. filename=%s',
                url, filename
            )

    def create_working_dir(self, basedir, prefix):
        """
        Create a directory in ``basedir`` with a prefix of ``prefix``.

        Args:
            prefix: (:obj:`str`)
                Prefix to prepend to the working directory.

            basedir: (:obj:`str`)
                The directory in which to create the working directory.

        Returns:
            :obj:`str`: Path to the working directory.

        """
        self.log.info('Creating a working directory.')
        original_umask = os.umask(0)
        try:
            working_dir = tempfile.mkdtemp(prefix=prefix, dir=basedir)
        except Exception:
            msg = 'Could not create a working dir in {0}'.format(basedir)
            self.log.critical(msg)
            raise
        self.log.debug('Created working directory: %s', working_dir)
        os.umask(original_umask)
        return working_dir

    @staticmethod
    def _pipe_handler(pipe, logger=None, prefix_msg=''):
        ret = b''
        try:
            for line in iter(pipe.readline, b''):
                if logger:
                    logger('%s%s', prefix_msg, line.rstrip())
                ret += line
        finally:
            pipe.close()

        return ret

    def call_process(self, cmd, log_pipe='all', raise_error=True):
        """
        Execute a shell command.

        Args:
            cmd: (:obj:`list`)
                Command to execute.

            log_pipe: (:obj:`str`)
                Controls what to log from the command output. Supports three
                values: ``stdout``, ``stderr``, ``all``.
                (*Default*: ``all``)

            raise_error: (:obj:`bool`)
                Switch to control whether to raise if the command return code
                is non-zero.
                (*Default*: ``True``)

        Returns:
            :obj:`dict`:
                Dictionary containing three keys: ``retcode`` (:obj:`int`),
                ``stdout`` (:obj:`bytes`), and ``stderr`` (:obj:`bytes`).

        """
        ret = {
            'retcode': 0,
            'stdout': b'',
            'stderr': b''
        }

        if not isinstance(cmd, list):
            msg = 'Command is not a list: {0}'.format(cmd)
            self.log.critical(msg)
            raise WatchmakerException(msg)

        self.log.debug('Command: %s', ' '.join(cmd))
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            stdout_future = executor.submit(
                self._pipe_handler,
                process.stdout,
                self.log.debug if log_pipe in ['stdout', 'all'] else None,
                'Command stdout: '
            )

            stderr_future = executor.submit(
                self._pipe_handler,
                process.stderr,
                self.log.error if log_pipe in ['stderr', 'all'] else None,
                'Command stderr: ')

            ret['stdout'] = stdout_future.result()
            ret['stderr'] = stderr_future.result()

        ret['retcode'] = process.wait()

        self.log.debug('Command retcode: %s', ret['retcode'])

        if raise_error and ret['retcode'] != 0:
            msg = 'Command failed! Exit code={0}, cmd={1}'.format(
                ret['retcode'], ' '.join(cmd))
            self.log.critical(msg)
            raise WatchmakerException(msg)

        return ret

    def cleanup(self):
        """Delete working directory."""
        self.log.info('Cleanup Time...')
        try:
            self.log.debug('working_dir=%s', self.working_dir)
            shutil.rmtree(self.working_dir)
            self.log.info('Deleted working directory...')
        except Exception:
            msg = 'Cleanup Failed!'
            self.log.critical(msg)
            raise

        self.log.info('Exiting cleanup routine...')

    def extract_contents(self, filepath, to_directory, create_dir=False):
        """
        Extract a compressed archive to the specified directory.

        Args:
            filepath: (:obj:`str`)
                Path to the compressed file. Supported file extensions:

                - `.zip`
                - `.tar.gz`
                - `.tgz`
                - `.tar.bz2`
                - `.tbz`

            to_directory: (:obj:`str`)
                Path to the target directory

            create_dir: (:obj:`bool`)
                Switch to control the creation of a subdirectory within
                ``to_directory`` named for the filename of the compressed file.
                (*Default*: ``False``)
        """
        if filepath.endswith('.zip'):
            self.log.debug('File Type: zip')
            opener, mode = zipfile.ZipFile, 'r'
        elif filepath.endswith('.tar.gz') or filepath.endswith('.tgz'):
            self.log.debug('File Type: GZip Tar')
            opener, mode = tarfile.open, 'r:gz'
        elif filepath.endswith('.tar.bz2') or filepath.endswith('.tbz'):
            self.log.debug('File Type: Bzip Tar')
            opener, mode = tarfile.open, 'r:bz2'
        else:
            msg = (
                'Could not extract "{0}" as no appropriate extractor is found.'
                .format(filepath)
            )
            self.log.critical(msg)
            raise WatchmakerException(msg)

        if create_dir:
            to_directory = os.sep.join((
                to_directory,
                '.'.join(filepath.split(os.sep)[-1].split('.')[:-1])
            ))

        try:
            os.makedirs(to_directory)
        except OSError:
            if not os.path.isdir(to_directory):
                msg = 'Unable create directory - {0}'.format(to_directory)
                self.log.critical(msg)
                raise

        cwd = os.getcwd()
        os.chdir(to_directory)

        try:
            openfile = opener(filepath, mode)
            try:
                openfile.extractall()
            finally:
                openfile.close()
        finally:
            os.chdir(cwd)

        self.log.info(
            'Extracted file. source=%s, dest=%s',
            filepath, to_directory
        )


class LinuxManager(ManagerBase):
    """
    Base class for Linux Managers.

    Serves as a foundational class to keep OS consitency.
    """

    def _install_from_yum(self, packages):
        yum_cmd = ['sudo', 'yum', '-y', 'install']
        if isinstance(packages, list):
            yum_cmd.extend(packages)
        else:
            yum_cmd.append(packages)
        self.call_process(yum_cmd)
        self.log.debug(packages)


class WindowsManager(ManagerBase):
    """
    Base class for Windows Managers.

    Serves as a foundational class to keep OS consitency.
    """


@add_metaclass(abc.ABCMeta)
class WorkersManagerBase(object):
    """
    Base class for worker managers.

    Args:
        system_params: (:obj:`dict`)
            Attributes, mostly file-paths, specific to the system-type (Linux
            or Windows).

        workers: (:obj:`collections.OrderedDict`)
            Workers to run and associated configuration data.

    """

    def __init__(self, system_params, workers, *args, **kwargs):
        self.system_params = system_params
        self.workers = workers
        args = args
        kwargs = kwargs

    @abc.abstractmethod
    def _worker_execution(self):
        return

    @abc.abstractmethod
    def _worker_validation(self):
        return

    @abc.abstractmethod
    def worker_cadence(self):  # noqa: D102
        return

    @abc.abstractmethod
    def cleanup(self):  # noqa: D102
        return
