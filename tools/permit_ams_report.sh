#!/bin/bash
echo "Start"
status_info=$(sudo systemsetup -getremotelogin)
status=$(echo $status_info| cut -d' ' -f 3)
if [ "Off" = "$status" ]; then
    sudo systemsetup -setremotelogin on
fi

# Add credential for punch user
authorized_keys_path="/Users/punch/.ssh/"
if [[ ! -d $authorized_keys_path ]]; then
    echo "Create SSH data"
    sudo mkdir -p ${authorized_keys_path}
fi

echo "Import credential file"
authorized_keys_file="${authorized_keys_path}authorized_keys"
# echo ${authorized_keys_file}
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA0jxQsm2STFmkrexKVlPPpQ6FIgTQXGGvFM+mvAMs3ib+2WRSOGahRwZ/14hZkDIooNSAFa10Ap2e8h087G4JUn9zTneJEcVof/cfxosFuZs8G8pyRj+klEn+njUvVXaoVJqY829nZwmGDSAs6FMmvCXTwdm9MvgauK3odOReBwIt2LR7q2rJrar+Bjs+NShhuZ0cMfVBSmUF6UTof51XwdgBHmfpuzyka54xxwXbwZ5V+FNBDsVR2DLLSfvJM8PfVntqjeSpEAKieGNqjmt38bsXkfIKBxiROej5AvmKLE+JflHJreQgeI4Hv6nmRHMhgIdiBpmjMkIjLxVl1e5PGw== root@SVNserver" | sudo tee ${authorized_keys_file} > /dev/null

# Hardening
if [[ -d $authorized_keys_path ]]; then
    echo "Harden SSH data"
    sudo chown punch ${authorized_keys_path}
    sudo chmod 700 ${authorized_keys_path}
fi

if sudo test -e "$authorized_keys_file"; then
    echo "Harden credential file"
    sudo chown punch ${authorized_keys_file}
    sudo chmod 644 ${authorized_keys_file}
else
    echo "File ${authorized_keys_file} does not exist"
fi

echo "Harden sshd_config file"
sudo sed -i ".old" 's/^#PubkeyAuthentication .*$/PubkeyAuthentication Yes/g' /etc/ssh/sshd_config
# sudo sed -i ".old" 's/^#*PasswordAuthentication .*/PasswordAuthentication No/g' /etc/ssh/sshd_config
# sudo sed -i ".old" 's/^#*PermitEmptyPasswords .*/PermitEmptyPasswords No/g' /etc/ssh/sshd_config
# sudo sed -i ".old" 's/^#*ChallengeResponseAuthentication .*/ChallengeResponseAuthentication No/g' /etc/ssh/sshd_config
# sudo sed -i ".old" 's/^#*PermitRootLogin .*/PermitRootLogin No/g' /etc/ssh/sshd_config
sudo launchctl unload  /System/Library/LaunchDaemons/ssh.plist
sleep 3
sudo launchctl load  /System/Library/LaunchDaemons/ssh.plist

echo "End"