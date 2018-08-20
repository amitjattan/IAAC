import sys
import uuid

#Get passed in arguments
print sys.argv

env_path = sys.argv[1]
ipAddress = sys.argv[2]
project = sys.argv[3]
env_parts = env_path.split('/')
environ = env_parts[1]
#tech, uuid = env_parts[2].split('-', 1) # TECH-UUID1-UUID2-UUIDN...
uuid = project
tech = 'JBOSS'

### instantiate Infra pieces

### get ref to jumpbox
#jumpBox = "Infrastructure/{}/TestJumpStation".format(environ)
#jumpBox_xld = repository.read(jumpBox)

overthereConfig = {
    'os': "UNIX",
    'connectionType': 'SCP',
    'address': ipAddress,
    'port': '22',
    'username': 'centos',
    'privateKeyFile': '/opt/apps/xl-deploy/ssh/tasakey.pem'
}

serverPath = "Infrastructure/{}/{}".format(environ, uuid)
overthere = factory.configurationItem(serverPath, "overthere.SshHost", overthereConfig)
repository.create(overthere)

if tech == "JBOSS":
    jbossStandaloneConfig = {
        'home': '/opt/jboss-eap-7.0/',
        'port': '9999',
        'enableDaemon': 'true',
        'adminHostAddress': 'localhost',
        'username': 'admin',
        'password': 'jboss-123',
        'tags': project,
    }
    jbossControllerPath = "{}/{}".format(serverPath, project)
    jbossStandalone=factory.configurationItem(jbossControllerPath,"jbossdm.StandaloneServer", jbossStandaloneConfig)
    jbossStandalone_xld = repository.create(jbossStandalone)

    envConfig = {
        'members': [jbossStandalone_xld.id],
        'dictionaries': []
    }
else:
    print("Unsupported Technology: {}".format(tech))
    exit()

env_path = "Environments/{}/{}-{}".format(environ, tech, uuid)
instanceEnv = factory.configurationItem(env_path, "udm.Environment", envConfig)
repository.create(instanceEnv)

# "return" Environment Path
print env_path
