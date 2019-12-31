Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.hostname = "dev.blogsite.com"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "1048"
  end

  config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  config.vm.synced_folder "app", "/app", owner: "blog", group: "blog"

  config.vm.network "private_network", ip: "192.186.20.20"

  config.vm.provision "file", source: "app/api/requirements", destination: "/tmp/"

end
