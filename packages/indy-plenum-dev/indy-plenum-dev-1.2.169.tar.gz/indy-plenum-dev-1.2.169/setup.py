import os
import sys

from setuptools import setup, find_packages

v = sys.version_info
if sys.version_info < (3, 5):
    msg = "FAIL: Requires Python 3.5 or later, " \
          "but setup.py was run using {}.{}.{}"
    v = sys.version_info
    print(msg.format(v.major, v.minor, v.micro))
    # noinspection PyPackageRequirements
    print("NOTE: Installation failed. Run setup.py using python3")
    sys.exit(1)

# Change to ioflo's source directory prior to running any command
try:
    SETUP_DIRNAME = os.path.dirname(__file__)
except NameError:
    # We're probably being frozen, and __file__ triggered this NameError
    # Work around this
    SETUP_DIRNAME = os.path.dirname(sys.argv[0])

if SETUP_DIRNAME != '':
    os.chdir(SETUP_DIRNAME)

SETUP_DIRNAME = os.path.abspath(SETUP_DIRNAME)

METADATA = os.path.join(SETUP_DIRNAME, 'plenum', '__metadata__.py')
# Load the metadata using exec() so we don't trigger an import of ioflo.__init__
exec(compile(open(METADATA).read(), METADATA, 'exec'))

BASE_DIR = os.path.join(os.path.expanduser("~"), ".plenum")
LOG_DIR = os.path.join(BASE_DIR, "log")
CONFIG_FILE = os.path.join(BASE_DIR, "plenum_config.py")

for path in [BASE_DIR, LOG_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        msg = "# Here you can create config entries according to your " \
              "needs.\n " \
              "# For help, refer config.py in the plenum package.\n " \
              "# Any entry you add here would override that from config " \
              "example\n"
        f.write(msg)

setup(
    name='indy-plenum-dev',
    version=__version__,
    description='Plenum Byzantine Fault Tolerant Protocol',
    long_description='Plenum Byzantine Fault Tolerant Protocol',
    url='https://github.com/hyperledger/indy-plenum',
    download_url='https://github.com/hyperledger/indy-plenum/tarball/{}'.
        format(__version__),
    author=__author__,
    author_email='hyperledger-indy@lists.hyperledger.org',
    license=__license__,
    keywords='Byzantine Fault Tolerant Plenum',
    packages=find_packages(exclude=['test', 'test.*', 'docs', 'docs*']) + [
        'data', ],
    package_data={
        '': ['*.txt', '*.md', '*.rst', '*.json', '*.conf', '*.html',
             '*.css', '*.ico', '*.png', 'LICENSE', 'LEGAL', 'plenum']},
    include_package_data=True,
    install_requires=['jsonpickle', 'ujson==1.33',
                      'prompt_toolkit==0.57', 'pygments',
                      'rlp', 'sha3', 'leveldb',
                      'ioflo==1.5.4', 'semver', 'base58', 'orderedset',
                      'sortedcontainers==1.5.7', 'psutil', 'pip',
                      'portalocker==0.5.7', 'pyzmq', 'raet',
                      'psutil', 'intervaltree', 'msgpack-python==0.4.6', 'indy-crypto==0.1.6'],
    extras_require={
        'stats': ['python-firebase'],
        'benchmark': ['pympler']
                    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-xdist'],
    scripts=['scripts/plenum', 'scripts/init_plenum_keys',
             'scripts/start_plenum_node',
             'scripts/generate_plenum_pool_transactions',
             'scripts/gen_steward_key', 'scripts/gen_node',
             'scripts/export-gen-txns', 'scripts/get_keys',
             'scripts/udp_sender', 'scripts/udp_receiver', 'scripts/filter_log',
             'scripts/log_stats',
             'scripts/init_bls_keys']
)

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        msg = "# Here you can create config entries according to your " \
              "needs.\n " \
              "# For help, refer config.py in the plenum module.\n " \
              "# Any entry you add here would override that from config " \
              "example\n"
        f.write(msg)


# TODO: This code should not be copied here.
import getpass
import os
import shutil
import sys


def getLoggedInUser():
    if sys.platform == 'wind32':
        return getpass.getuser()
    else:
        if 'SUDO_USER' in os.environ:
            return os.environ['SUDO_USER']
        else:
            return getpass.getuser()


def changeOwnerAndGrpToLoggedInUser(directory, raiseEx=False):
    loggedInUser = getLoggedInUser()
    try:
        shutil.chown(directory, loggedInUser, loggedInUser)
    except Exception as e:
        if raiseEx:
            raise e
        else:
            pass


changeOwnerAndGrpToLoggedInUser(BASE_DIR)
changeOwnerAndGrpToLoggedInUser(LOG_DIR)
