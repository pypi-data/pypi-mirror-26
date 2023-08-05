
from ..runtimetool import RuntimeTool
from .bashtoolmixin import BashToolMixIn


class nodeTool(BashToolMixIn, RuntimeTool):
    """Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

Home: https://nodejs.org/en/

Notes on tuning:
* .tune.nodeArgs

Note: NODE_ENV is set based on nodeEnv or .env.type
"""
    __slots__ = ()

    def getDeps(self):
        if self._detect.isAlpineLinux():
            return []

        return ['nvm', 'bash']

    def _installTool(self, env):
        if self._detect.isAlpineLinux():
            if env['nodeVer'] == 'current':
                self._install.apk('nodejs-current')
            else:
                self._install.apk('nodejs')
            return

        self._callBash(env,
                       'source {0} --no-use && nvm install {1}'
                       .format(env['nvmInit'], env['nodeVer']))

    def _updateTool(self, env):
        self._installTool(env)

    def uninstallTool(self, env):
        self._callBash(env,
                       'source {0} --no-use && nvm deactivate && nvm uninstall {1}'
                       .format(env['nvmInit'], env['nodeVer']))
        self._have_tool = False

    def envNames(self):
        return ['nodeBin', 'nodeVer', 'nodeEnv']

    def initEnv(self, env):
        node_version = env.setdefault('nodeVer', 'stable')
        #---
        node_env = env.get('nodeEnv', '')

        if node_env:
            pass
        elif env['type'] == 'dev':
            node_env = 'development'
        else:
            node_env = 'production'

        self._environ['NODE_ENV'] = node_env
        #---

        if self._detect.isAlpineLinux():
            super(nodeTool, self).initEnv(env)
            return

        try:
            env_to_set = self._callBash(env,
                                        'source {0} --no-use && \
                nvm use {1} >/dev/null && \
                env | egrep "^(NVM_|PATH=)"'
                                        .format(env['nvmInit'], node_version),
                                        verbose=False
                                        )
        except:
            return

        if env_to_set:
            self._pathutil.updateEnvFromOutput(env_to_set)
            super(nodeTool, self).initEnv(env)
            self._environ['nodeVer'] = node_version

    def tuneDefaults(self, env):
        return {
            'minMemory': '64M',
            'debugOverhead': '32M',
            'connMemory': '32K',
            'debugConnOverhead': '64K',
            'socketTypes': ['unix', 'tcp', 'tcp6'],
            'socketType': 'unix',
            'scalable': True,
            'multiCore': False,
            'maxRequestSize': '1M',
            'socketProtocol': 'http',
        }

    def onRun(self, config, svc, args):
        svc_tune = svc['tune']

        #---
        node_env = {}

        try:
            if svc_tune['socketType'] == 'unix':
                node_env['PORT'] = svc_tune['socketPath']
            else:
                node_env['PORT'] = str(svc_tune['socketPort'])
                node_env['HOST'] = svc_tune['socketAddress']
        except KeyError:
            pass

        self._environ.update(node_env)

        #---
        node_args = []

        if 'maxMemory' in svc_tune:
            heap_limit = self._configutil.parseMemory(svc_tune['maxMemory'])
            heap_limit = int(heap_limit * 0.9)
            heap_limit = int(heap_limit // 1024 // 1024)

            node_args.append(
                '--max_old_space_size={0}'.format(heap_limit)
            )

        #---

        cmd = [
            config['env']['nodeBin'],
            svc['path']
        ] + node_args + args

        self._executil.callInteractive(cmd)
