IMAGE_NAME = "centos/7"
N = 2
INET = "kubernetes_network"
ANSIBLE_SERVERIP = "172.16.10.240"
K8SMASTER_IP = "172.16.25.200"
K8SWORKER_IP = "172.16.25."
MASTER_NODE_RAM = 8192
MASTER_NODE_CPU = 4
WORKER_NODE_RAM = 16384
WORKER_NODE_CPU = 6

Vagrant.configure("2") do |config|
  config.ssh.insert_key = false

  # master node
  config.vm.define "k8s-master" do |cfg|
    cfg.vm.box = IMAGE_NAME
    cfg.vm.network "private_network", ip: K8SMASTER_IP, virtualbox__intnet: INET
    cfg.vm.hostname = "k8s-master"
    
    cfg.vm.provider "virtualbox" do |v|
      v.memory = MASTER_NODE_RAM
      v.cpus = MASTER_NODE_CPU
      v.name = "k8s-master"
    end
    cfg.vm.provision "shell", inline: <<-SCRIPT
      sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
      systemctl restart sshd
    SCRIPT
  end

  # worker node
  (1..N).each do |i|
    config.vm.define "k8s-worekr-#{i}" do |cfg|
      cfg.vm.box = IMAGE_NAME
      cfg.vm.network "private_network", ip: K8SWORKER_IP + "#{i+10}", virtualbox__intnet: INET
      cfg.vm.hostname = "k8s-worker-#{i}"
      
      cfg.vm.provider "virtualbox" do |v|
        v.memory = WORKER_NODE_RAM
        v.cpus = WORKER_NODE_CPU
        v.name = "k8s-worker-#{i}"
      end
      cfg.vm.provision "shell", inline: <<-SCRIPT
        sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
        systemctl restart sshd
      SCRIPT
    end
  end


  # ansible-server
  config.vm.define "ansible-server4" do |cfg|
    cfg.vm.box = IMAGE_NAME
    cfg.vm.hostname = "ansible-server-4"
    cfg.vm.network "private_network", ip: ANSIBLE_SERVERIP, virtualbox__intnet: INET

    cfg.vm.provider "virtualbox" do |v|
      v.memory = 2048
      v.cpus = 2
      v.name =  "ansible-server-4"
    end
    cfg.vm.provision  "shell", inline: <<-SCRIPT
      yum install epel-release -y
      yum install python36 libselinux-python3 -y 
      yum install sshpass -y
      pip3 install ansible
      pip3 install -U pip
      sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
      systemctl restart sshd
    SCRIPT

    # copy ansible files
    cfg.vm.provision "file", source: "./ansible_workspace", destination: "ansible_workspace"
    cfg.vm.provision "shell", inline: "ansible-playbook ./ansible_workspace/add_hosts.yaml", privileged: false
    cfg.vm.provision "shell", inline: "ansible-playbook ./ansible_workspace/configure_ssh.yaml -i /home/vagrant/hosts", privileged: false

    # run k8s-master role                               
    cfg.vm.provision "shell", inline: "ansible-playbook ./ansible_workspace/roles/k8s_master/site.yml -i /home/vagrant/hosts", privileged: false

    # run k8s-worker role
    cfg.vm.provision "shell", inline: "ansible-playbook ./ansible_workspace/roles/k8s_worker/site.yml -i /home/vagrant/hosts", privileged: false
  end
end
