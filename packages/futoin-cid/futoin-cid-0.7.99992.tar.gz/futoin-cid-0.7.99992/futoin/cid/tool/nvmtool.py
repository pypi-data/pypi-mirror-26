
from ..runenvtool import RunEnvTool
from .bashtoolmixin import BashToolMixIn


class nvmTool(BashToolMixIn, RunEnvTool):
    """Node Version Manager.

Home: https://github.com/creationix/nvm    
"""
    __slots__ = ()

    NVM_LATEST = '$(git describe --abbrev=0 --tags --match "v[0-9]*")'

    def getDeps(self):
        return ['bash', 'git']

    def _installTool(self, env):
        nvm_dir = env['nvmDir']
        nvm_git = env.get('nvmGit', 'https://github.com/creationix/nvm.git')
        nvm_ver = env.get('nvmVer', self.NVM_LATEST)

        self._callBash(env,
                       'git clone {1} {0}; \
               cd {0} && git fetch && git reset --hard && git checkout {2}'
                       .format(nvm_dir, nvm_git, nvm_ver))

    def _updateTool(self, env):
        nvm_dir = env['nvmDir']
        nvm_ver = env.get('nvmVer', self.NVM_LATEST)

        self._callBash(env,
                       'cd {0} && git fetch && git reset --hard && git checkout {1}'
                       .format(nvm_dir, nvm_ver))

    def uninstallTool(self, env):
        nvm_dir = env['nvmDir']
        self._pathutil.rmTree(nvm_dir)
        self._have_tool = False

    def envNames(self):
        return ['nvmDir', 'nvmGit', 'nvmVer']

    def initEnv(self, env):
        ospath = self._ospath
        nvm_dir = ospath.join(self._environ['HOME'], '.nvm')
        nvm_dir = env.setdefault('nvmDir', nvm_dir)
        env_init = ospath.join(nvm_dir, 'nvm.sh')
        env['nvmInit'] = env_init
        self._have_tool = ospath.exists(env_init)

    def onExec(self, env, args, replace=True):
        cmd = '. {0} && nvm {1}'.format(
            env['nvmInit'], self._ext.subprocess.list2cmdline(args))
        self._callBashInteractive(env, cmd, replace=replace)
