import sys

#Get passed in arguments
if len(sys.argv)!= 2:
    print ("Script requires 1 parameter (environment name)")
    exit()

env_path = sys.argv[1]
env_parts = env_path.split('/')
environ = env_parts[1]
tech, uuid = env_parts[2].split('-', 1) # TECH-UUID1-UUID2-UUIDN...

# Delete environment
if repository.exists(env_path):
    repository.delete(env_path)

# Delete infrastructure
if tech == 'JBOSS':
    jbossServerPath = "Infrastructure/{}/{}".format(environ, uuid)
    jbossControllerPath = "{}/{}".format(jbossServerPath, 'JBoss-Controller')
    jbossSgPath = "{}/{}".format(jbossControllerPath, 'mike-server-group')

    if repository.exists(jbossSgPath):
        repository.delete(jbossSgPath)
    if repository.exists(jbossControllerPath):
        repository.delete(jbossControllerPath)
    if repository.exists(jbossServerPath):
        repository.delete(jbossServerPath)
