# -*- coding: utf-8 -*-
import os
import logging
from crosspm.helpers.package import Package
from crosspm.helpers.exceptions import *
from crosspm.helpers.config import CROSSPM_DEPENDENCY_FILENAME, CROSSPM_DEPENDENCY_LOCK_FILENAME
from crosspm.helpers.parser import Parser


def update_progress(msg, progress):
    sys.stderr.write('\r{0} [{1:10}] {2}%'.format(msg, '#' * int(float(progress) / 10.0), int(progress)))
    sys.stderr.flush()


class Downloader:
    def __init__(self, config, do_load=True):
        self._packages = {}
        self._log = logging.getLogger('crosspm')
        self._config = config
        self.cache = config.cache
        self.solid = config.solid
        self._root_package = Package('<root>', 0, {self._config.name_column: '<root>'}, self, None,
                                     Parser('common', {}, config))

        # self._cache_path = config.crosspm_cache_root
        # if not os.path.exists(self._cache_path):
        #     os.makedirs(self._cache_path)

        # self.packed_path = os.path.realpath(os.path.join(self._cache_path, 'archive'))
        # self.unpacked_path = os.path.realpath(os.path.join(self._cache_path, 'cache'))
        # self.temp_path = os.path.realpath(os.path.join(self._cache_path, 'tmp'))

        if not config.deps_path:
            config.deps_path = \
                config.deps_file_name if config.deps_file_name else CROSSPM_DEPENDENCY_FILENAME
        deps_path = config.deps_path.strip().strip('"').strip("'")
        self._deps_path = os.path.realpath(os.path.expanduser(deps_path))

        if not config.depslock_path:
            config.depslock_path = \
                config.deps_lock_file_name if config.deps_lock_file_name else CROSSPM_DEPENDENCY_LOCK_FILENAME
        depslock_path = config.depslock_path.strip().strip('"').strip("'")
        self._depslock_path = os.path.realpath(os.path.expanduser(depslock_path))

        self.do_load = do_load

    # Get list of all packages needed to resolve all the dependencies.
    # List of Package class instances.
    def get_packages(self, list_or_file_path=None):
        if list_or_file_path is None:
            list_or_file_path = self._depslock_path
            if not os.path.isfile(list_or_file_path):
                list_or_file_path = self._deps_path

        _packages = {}
        if isinstance(list_or_file_path, str):
            self._log.info('Reading dependencies ... [%s]', list_or_file_path)
        for i, _src in enumerate(self._config.sources()):
            if i > 0:
                self._log.info('')
                self._log.info('Next source ...')
            _found_packages = _src.get_packages(self, list_or_file_path)
            _packages.update(
                {k: v for k, v in _found_packages.items() if _packages.get(k, None) is None})
            if not self._config.no_fails:
                if isinstance(list_or_file_path, (list, tuple)):
                    list_or_file_path = [x for x in list_or_file_path if
                                         _packages.get(x[self._config.name_column], None) is None]
                elif isinstance(list_or_file_path, dict) and isinstance(list_or_file_path.get('raw', None), list):
                    list_or_file_path['raw'] = [x for x in list_or_file_path['raw'] if
                                                _packages.get(x[self._config.name_column], None) is None]

        return _packages

    # Download packages or just unpack already loaded (it's up to adapter to decide)
    def download_packages(self, depslock_file_path=None):
        if depslock_file_path is None:
            depslock_file_path = self._depslock_path
        if isinstance(depslock_file_path, str):
            if not os.path.isfile(depslock_file_path):
                depslock_file_path = self._deps_path

        self._log.info('Check dependencies ...')
        # print_stdout('Check dependencies ...')

        self._packages = {}
        self._root_package.find_dependencies(depslock_file_path)

        self._log.info('')
        self._log.info('Dependency tree:')
        self._root_package.print(0, self._config.output('tree', [{self._config.name_column: 0}]))

        _not_found = any(_pkg is None for _pkg in self._packages.values())

        if not _not_found and self.do_load:
            self._log.info('Unpack ...')

            total = len(self._packages)
            for i, _pkg in enumerate(self._packages.values()):
                update_progress('Download/Unpack:', float(i) / float(total) * 100.0)
                if _pkg.download():  # self.packed_path):
                    _pkg.unpack()  # self.unpacked_path)

            update_progress('Download/Unpack:', 100)
            print_stdout('')
            self._log.info('Done!')
            sys.stdout.write('\n')
            sys.stdout.write('\n')
            sys.stdout.flush()

            if self._config.lock_on_success:
                from crosspm.helpers.locker import Locker
                depslock_path = os.path.realpath(
                    os.path.join(os.path.dirname(depslock_file_path), self._config.deps_lock_file_name))
                Locker(
                    self._config,
                    self._packages if self._config.recursive else self._root_package.packages,
                ).lock_packages(depslock_file_path, depslock_path)

        return self._packages

    def add_package(self, pkg_name, package):
        _added = False
        if self._config.no_fails and package is not None:
            pkg_name = package.set_full_unique_name()
        if pkg_name in self._packages:
            if self._packages[pkg_name] is None:
                _added = True
            elif (package is not None) and (not self._config.no_fails):
                param_list = self._config.get_fails('unique', {})
                params1 = self._packages[pkg_name].get_params(param_list)
                params2 = package.get_params(param_list)
                for x in param_list:
                    # START HACK for cached archive
                    param1 = params1[x]
                    param2 = params2[x]
                    if isinstance(param1, list):
                        param1 = [str(x) for x in param1]
                    if isinstance(param2, list):
                        param2 = [str(x) for x in param2]
                    # END

                    if str(param1) != str(param2):
                        raise CrosspmException(
                            CROSSPM_ERRORCODE_MULTIPLE_DEPS,
                            'Multiple versions of package "{}" found in dependencies.'.format(pkg_name),
                        )
        else:
            _added = True
        if _added:
            self._packages[pkg_name] = package

        return _added, self._packages[pkg_name]

    def get_raw_packages(self):
        return self._root_package.packages
