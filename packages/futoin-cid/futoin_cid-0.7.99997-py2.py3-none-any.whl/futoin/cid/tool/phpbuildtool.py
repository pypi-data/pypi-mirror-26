
from ..runenvtool import RunEnvTool
from .bashtoolmixin import BashToolMixIn


class phpbuildTool(BashToolMixIn, RunEnvTool):
    """Builds PHP so that multiple versions can be used side by side.

Home: https://github.com/php-build/php-build
"""
    __slots__ = ()

    PHPBUILD_LATEST = 'master'

    def getDeps(self):
        return ['bash', 'git']

    def _installTool(self, env):
        phpbuild_dir = env['phpbuildDir']
        phpbuild_git = env.get(
            'phpbuildGit', 'https://github.com/php-build/php-build.git')
        phpbuild_ver = env.get('phpbuildVer', self.PHPBUILD_LATEST)

        self._callBash(env,
                       'git clone {1} {0}; \
               cd {0} && git fetch && git reset --hard && git checkout {2}'
                       .format(phpbuild_dir, phpbuild_git, phpbuild_ver))

    def _updateTool(self, env):
        if env.get('phpBinOnly', False):
            return

        phpbuild_dir = env['phpbuildDir']
        phpbuild_ver = env.get('phpbuildVer', self.PHPBUILD_LATEST)

        self._callBash(env,
                       'cd {0} && git fetch && git reset --hard && git checkout {1} && git pull --rebase'
                       .format(phpbuild_dir, phpbuild_ver))

    def uninstallTool(self, env):
        phpbuild_dir = env['phpbuildDir']
        self._pathutil.rmTree(phpbuild_dir)
        self._have_tool = False

    def envNames(self):
        return ['phpbuildDir', 'phpbuildBin', 'phpbuildGit', 'phpbuildVer']

    def initEnv(self, env):
        ospath = self._ospath
        phpbuild_dir = ospath.join(self._environ['HOME'], '.phpbuild')
        phpbuild_dir = env.setdefault('phpbuildDir', phpbuild_dir)
        phpbuild_bin = env.setdefault(
            'phpbuildBin', ospath.join(phpbuild_dir, 'bin', 'php-build'))
        self._have_tool = ospath.exists(phpbuild_bin)

        # special case when environment required binaries only
        if env.get('phpBinOnly', False):
            self._have_tool = True
