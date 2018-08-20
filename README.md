# Things to remember while using or updating this repository.
1. In config.csv file for binary values put "Y" wherever it is needed and keep every other binary value "N".
2. While you are putting "Y" for removeInfra, you can not put "Y" for create infra and vice versa.
3. If you use withTestData "Y", must provide the s3 link from where It needs to download the data.
4. If you want to deploy the code with "Y" provide application name which must be similar to git repository name of that application.
5. If you are writing any role, rolename must be similar to the value of role variable which is being passed in Jenkinsfile.
