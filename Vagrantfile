require 'yaml'

CONFIG = YAML.load_file(File.join(File.dirname(__FILE__), 'config.yml'))

Vagrant.configure("2") do |config|
  config.ssh.insert_key = false

  # # master node
  # config.vm.define "k8s-master" do |cfg|
  #   cfg.vm.box = IMAGE_NAME
  #   cfg.vm.network "public_network", ip: K8Scontrolplane_IP
  #   cfg.vm.hostname = "k8s-master"
    
  #   cfg.vm.provider "virtualbox" do |v|
  #     v.memory = MASTER_NODE_RAM
  #     v.cpus = MASTER_NODE_CPU
  #     v.name = "k8s-master"
  #   end
  #   cfg.vm.provision "shell", inline: <<-SCRIPT
  #     sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
  #     systemctl restart sshd
  #   SCRIPT
  # end

  # # worker node
  # (1..N).each do |i|
  #   config.vm.define "k8s-worekr-#{i}" do |cfg|
  #     cfg.vm.box = IMAGE_NAME
  #     cfg.vm.network "public_network", ip: K8SWORKER_IP + "#{i+10}"
  #     cfg.vm.hostname = "k8s-worker-#{i}"
      
  #     cfg.vm.provider "virtualbox" do |v|
  #       v.memory = WORKER_NODE_RAM
  #       v.cpus = WORKER_NODE_CPU
  #       v.name = "k8s-worker-#{i}"
  #     end
  #     cfg.vm.provision "shell", inline: <<-SCRIPT
  #       sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
  #       systemctl restart sshd
  #     SCRIPT
  #   end
  # end


  # bootstrap-server
  config.vm.define CONFIG['vagrant-bootstrap']['name'] do |cfg|
    cfg.vm.box = CONFIG['vagrant-bootstrap']['box']
    cfg.vm.hostname = CONFIG['vagrant-bootstrap']['hostname']
    cfg.vm.network "public_network", ip: CONFIG['vagrant-bootstrap']['ip']

    cfg.vm.provider "virtualbox" do |v|
      v.memory = CONFIG['vagrant-bootstrap']['memory']
      v.cpus = CONFIG['vagrant-bootstrap']['cpu']
      v.name = CONFIG['vagrant-bootstrap']['hostname']
    end
    cfg.vm.provision  "shell", inline: <<-SCRIPT
      yum install epel-release -y
      yum install python36 libselinux-python3 -y 
      yum install sshpass -y
      pip3 install -U pip
      pip3 install ansible
      sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
      systemctl restart sshd
    SCRIPT

    # copy ansible files
    # cfg.vm.provision "file", source: "./ansible_workspace", destination: "ansible_workspace"
    # cfg.vm.provision "shell", inline: "ansible-playbook ./ansible_workspace/add_hosts.yaml", privileged: false
    # cfg.vm.provision "shell", inline: "ansible-playbook ./ansible_workspace/configure_ssh.yaml -i /home/vagrant/hosts", privileged: false

    # # run k8s-master role                               
    # cfg.vm.provision "shell", inline: "ansible-playbook ./ansible_workspace/roles/k8s_master/site.yml -i /home/vagrant/hosts", privileged: false

    # # run k8s-worker role
    # cfg.vm.provision "shell", inline: "ansible-playbook ./ansible_workspace/roles/k8s_worker/site.yml -i /home/vagrant/hosts", privileged: false
  end
end
