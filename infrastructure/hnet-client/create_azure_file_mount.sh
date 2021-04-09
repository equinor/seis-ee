# code from: https://docs.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-linux


# step 1: Create a folder for the mount point

resourceGroupName="CCS"
storageAccountName="ccs"
fileShareName="dev-ccs-passive"

mntPath="/archive"
sudo mkdir $mntPath


# step 2: Create a credential file to store the username (the storage account name) and password (the storage account key) for the file share.
if [ ! -d "/etc/smbcredentials" ]; then
    sudo mkdir "/etc/smbcredentials"
fi

storageAccountKey=$(az storage account keys list \
    --resource-group $resourceGroupName \
    --account-name $storageAccountName \
    --query "[0].value" | tr -d '"')

smbCredentialFile="/etc/smbcredentials/$storageAccountName.cred"
if [ ! -f $smbCredentialFile ]; then
    echo "username=$storageAccountName" | sudo tee $smbCredentialFile > /dev/null
    echo "password=$storageAccountKey" | sudo tee -a $smbCredentialFile > /dev/null
else 
    echo "The credential file $smbCredentialFile already exists, and was not modified."
fi


# step 3: Change permissions on the credential file so only root can read or modify the password file. 
sudo chmod 600 $smbCredentialFile


# step 4: Use the following command to append the following line to /etc/fstab
# This command assumes you have logged in with az login
httpEndpoint=$(az storage account show \
    --resource-group $resourceGroupName \
    --name $storageAccountName \
    --query "primaryEndpoints.file" | tr -d '"')
smbPath=$(echo $httpEndpoint | cut -c7-$(expr length $httpEndpoint))$fileShareName

if [ -z "$(grep $smbPath\ $mntPath /etc/fstab)" ]; then
    echo "$smbPath $mntPath cifs nofail,vers=3.0,credentials=$smbCredentialFile,serverino" | sudo tee -a /etc/fstab > /dev/null
else
    echo "/etc/fstab was not modified to avoid conflicting entries as this Azure file share was already present. You may want to double check /etc/fstab to ensure the configuration is as desired."
fi

sudo mount -a

