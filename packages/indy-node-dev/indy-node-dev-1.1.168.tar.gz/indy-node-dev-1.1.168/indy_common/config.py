import os
import logging
from collections import OrderedDict

from plenum.common.constants import ClientBootStrategy, HS_LEVELDB, KeyValueStorageType
from plenum.config import pool_transactions_file_base, domain_transactions_file_base

from indy_common.constants import Environment

nodeReg = OrderedDict([
    ('Alpha', ('127.0.0.1', 9701)),
    ('Beta', ('127.0.0.1', 9703)),
    ('Gamma', ('127.0.0.1', 9705)),
    ('Delta', ('127.0.0.1', 9707))
])

cliNodeReg = OrderedDict([
    ('AlphaC', ('127.0.0.1', 9702)),
    ('BetaC', ('127.0.0.1', 9704)),
    ('GammaC', ('127.0.0.1', 9706)),
    ('DeltaC', ('127.0.0.1', 9708))
])

baseDir = "~/.indy"

ENVS = {
    "test": Environment(pool_transactions_file_base + "_sandbox",
                        domain_transactions_file_base + "_sandbox"),
    "live": Environment(pool_transactions_file_base + "_live",
                        domain_transactions_file_base + "_live")
}

current_env = "test"
domainTransactionsFile = ENVS[current_env].domainLedger
poolTransactionsFile = ENVS[current_env].poolLedger
configTransactionsFile = "config_transactions"

logFilePath = "cli.log"

outFilePath = "cli_output.log"

clientBootStrategy = ClientBootStrategy.Custom

hashStore = {
    "type": HS_LEVELDB
}

primaryStorage = None

configStateStorage = KeyValueStorageType.Leveldb
idrCacheStorage = KeyValueStorageType.Leveldb
attrStorage = KeyValueStorageType.Leveldb

configStateDbName = 'config_state'
attrDbName = 'attr_db'
idrCacheDbName = 'idr_cache_db'

RAETLogLevel = "concise"
RAETLogLevelCli = "mute"
RAETLogFilePath = os.path.join(os.path.expanduser(baseDir), "raet.log")
RAETLogFilePathCli = None
RAETMessageTimeout = 30


PluginsToLoad = []


# TODO: This should be in indy_node's config

# File that stores the version of the Node ran the last time it started. (It
# might be incorrect sometimes if Node failed to update the file and crashed)
lastRunVersionFile = 'last_version'


# File that stores the version of the code to which the update has to be made.
# This is used to detect if there was an error while upgrading. Once it has
# been found out that there was error while upgrading, then it can be upgraded.
nextVersionFile = 'next_version'


# Minimum time difference (seconds) between the code update of 2 nodes
MinSepBetweenNodeUpgrades = 300


upgradeLogFile = "upgrade_log"

lastVersionFilePath = "last_version_file"

'''
Node control utils options
'''
controlServiceHost = "127.0.0.1"
controlServicePort = "30003"


'''
logging level for agents
'''
agentLoggingLevel = logging.INFO
'''
default logging level for node
'''
logLevel = logging.INFO
