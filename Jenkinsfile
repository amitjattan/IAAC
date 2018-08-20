pipeline {
    agent {
    node {
        label 'hlblbdgtd101'
  }
}
stages {
        stage('Create AWS Infra') {
            steps {
            
            withCredentials([string(credentialsId: '55b0db94-7f76-44a9-84a6-bfdfd847cb42', variable: 'access_key'), string(credentialsId: '6e1d4925-0425-4d95-9b6a-b0680ac15442', variable: 'secret_key'), usernameColonPassword(credentialsId: '40197464-570a-4c9b-97d1-5a9af7c834b1', variable: 'credential'), usernamePassword(credentialsId: '9c6bf829-1dd3-46f5-9aa4-7f6386e6b748', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME'), usernamePassword(credentialsId: '211034b1-52e8-4d0f-953e-923716c6cff8' , passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
	    	sh '''
	    		export http_proxy=https://proxy.standard.com:8080
	    		export https_proxy=https://proxy.standard.com:8080
	    		export AWS_ACCESS_KEY_ID="${access_key}"
            		export AWS_SECRET_ACCESS_KEY="${secret_key}"
                
		if [ ! -e "IAAC/bin/activate" ] 
		then


			~/.local/bin/pip install virtualenv --user
			~/.local/bin/virtualenv --system-site-packages IAAC
		fi
		if [ ! -e "terraform" ] 
		then
			wget https://releases.hashicorp.com/terraform/0.11.0/terraform_0.11.0_linux_amd64.zip
			unzip terraform_0.11.0_linux_amd64.zip
			chmod +x terraform
		fi


		if [ ! -e "packer" ]
		then
			wget https://releases.hashicorp.com/packer/1.1.2/packer_1.1.2_linux_amd64.zip
			unzip packer_1.1.2_linux_amd64.zip
			chmod +x packer

		fi
	
		if [ ! -e "xl-deploy-6.0.3-cli" ]
		then
			cli_url='https://nexus.standard.com:8443/nexus/repository/bre-m2/com/standard/bre/com/xebialabs/xl-deploy/6.0.3/xl-deploy-6.0.3-cli.zip'
               		curl --fail --silent --show-error --junk-session-cookies --location \$cli_url > cli.zip
               		unzip -qo cli.zip
		fi

	source IAAC/bin/activate

	{
		read
		while read -r line
	do
		platform=$(echo "$line" |awk -F "," '{ print $1 }')
		version=$(echo "$line" |awk -F "," '{ print $2 }')
		package=$(echo "$line" |awk -F "," '{ print $3 }')
		allowed_port=$(echo "$line" |awk -F "," '{ print $4 }')
		db_With_TestData=$(echo "$line" |awk -F "," '{ print $6 }')
		s3_Data_Link=$(echo "$line" |awk -F "," '{ print $7 }')
		project=$(echo "$line" |awk -F "," '{ print $8 }')
		environment=$(echo "$line" |awk -F "," '{ print $9 }')
		Deployment=$(echo "$line" |awk -F "," '{ print $11 }')
		appName=$(echo "$line" |awk -F "," '{ print $12 }')

		infra=$(echo "$line" |awk -F "," '{ print $5 }')
		if [ "$infra" == "Y" ];then
			##if ["$db_With_Testdata" == "Y"];then
			#	./packer validate "packer.json"
			#	./packer build -machine-readable -force -var "aws_access_key=${access_key}" -var "aws_secret_key=${secret_key}" -var "role=${platform}-${version}-WithTestData" -var "ami_name=${project}_${platform}_${version}_${environment}" "packer.json" | tee packer.log
			#	curl -v -u ${credential} --insecure --upload-file manifest.json https://nexus-dev.standard.com:8443/nexus/repository/Infra-AMI-IDs/${project}_${platform}_${version}_${environment}_WithTestData/manifest.json
			#else
			##var_ami_name=${project}_${platform}_${version}_${environment}
			##ami_name=$(echo "$var_ami_name")
			##rm -f ./${package}
			##wget https://nexus.standard.com:8443/nexus/repository/bre-raw/packer/${package}
			##./packer validate "./iaacScripts/packer.json"
			##./packer build -machine-readable -force -var "aws_access_key=${access_key}" -var "aws_secret_key=${secret_key}" -var "role=${platform}-${version}" -var "ami_name=${ami_name}" -var "package=${package}" "./iaacScripts/packer.json" | tee packer.log
			##curl -v -u ${credential} --insecure --upload-file manifest.json https://nexus-dev.standard.com:8443/nexus/repository/Infra-AMI-IDs/${project}_${platform}_${version}_${environment}/manifest.json
			#fi
			##rm -f manifest.*
			##wget https://nexus-dev.standard.com:8443/nexus/repository/Infra-AMI-IDs/${project}_${platform}_${version}_${environment}/manifest.json
			Oami_id=$(cat manifest.json | awk -F'"artifact_id": "us-west-2:' '{print $2}' | awk -F'",' '{print $1}' |tr -d '[:space:]') 
			ami_id=$(echo "$Oami_id")
			cd iaacScripts
			../terraform init -lock=false -force-copy -backend=true -backend-config="key=tfstates/${project}_${platform}_${version}_${environment}/terraform.tfstate"
			../terraform get
			../terraform plan -lock=false -var "access_key=${access_key}" -var "secret_key=${secret_key}" -var "tag=${project}_${platform}_${version}_${environment}" -var "ami=${ami_id}" -var "port=${allowed_port}" -var "count=1" -var "sg_name=${platform}_IAAC"
			../terraform apply --auto-approve -lock=false -var "access_key=${access_key}" -var "secret_key=${secret_key}" -var "tag=${project}_${platform}_${version}_${environment}" -var "ami=${ami_id}" -var "port=${allowed_port}" -var "count=1" -var "sg_name=${platform}_IAAC"
			ipAddress=$(../terraform output private_ip)
			cd ../
			if [ "$Deployment" == "Y" ];then
				workspace=$(pwd)
                		export PATH="$workspace/xl-deploy-6.0.3-cli/bin:$PATH"
				cli.sh -username $USERNAME -password $PASSWORD -quiet \
                        	-secure -host xldeploy-dev.standard.com -port 4517 \
                        	-source "$workspace/iaacScripts/xl-deploy/DynXldInfraCreationForAwsInstances.py" "Environments/INT/${platform}" "${ipAddress}" "${project}"
				git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.standard.com/BRE-Samples-Dev/${appName}.git && cd ${appName} && echo "DummyCommit" >> README.md && git add --all && git commit -m "Dummy Commit" && git push

			fi

		fi

		removeInfra=$(echo "$line" |awk -F "," '{ if ($5=="N") print $10; }')
		echo "$removeInfra"
		if [ "$removeInfra" == "Y" ];then
			cd iaacScripts
			../terraform plan -var "access_key=${access_key}" -var "secret_key=${secret_key}" -var "tag=${project}_${platform}_${version}_${environment}" -var "ami=${ami_id}" -var "port=${allowed_port}" -var "count=0" -var "sg_name=${platform}_IAAC"
			../terraform apply --auto-approve -var "access_key=${access_key}" -var "secret_key=${secret_key}" -var "tag=${project}_${platform}_${version}_${environment}" -var "ami=${ami_id}" -var "port=${allowed_port}" -var "count=0" -var "sg_name=${platform}_IAAC"
		fi
		
	done 
	} < config.csv
	'''
}
            }
        }
    }
}
