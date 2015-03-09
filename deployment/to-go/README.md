# ElSA to-go: Playa Mesos-based Vagrant deployment

ElSA to-go is derived from [Playa Mesos][5] which in turn relies on [VirtualBox][3], [Vagrant][4], and an Ubuntu box image which has [Mesos][1] and [Marathon][2] pre-installed. As an alternative to VirtualBox, it's possible to build and run the image on
VMware [Fusion](https://www.vmware.com/products/fusion/) or [Workstation](https://www.vmware.com/products/workstation/).

## Requirements

* [VirtualBox][3] 4.2+
* [Vagrant][4] 1.3+
* VMware [Fusion](https://www.vmware.com/products/fusion/) or [Workstation](https://www.vmware.com/products/workstation/) (optional)

## Quick Start

1. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads)

1. [Install Vagrant](http://www.vagrantup.com/downloads.html)

1. Clone this repository

  ```bash
  git clone https://github.com/mhausenblas/elsa.git
  cd elsa/deployment/to-go
  ```

1. Start the VM

  ```bash
  vagrant up
  ```

1. Connect to the Mesos Web UI on [10.141.141.10:5050](http://10.141.141.10:5050) and the Marathon Web UI on [10.141.141.10:8080](http://10.141.141.10:8080)

1. SSH to the VM

  ```bash
  vagrant ssh
  ls -al
  exit
  ```
  
At this point in time you can [launch ElSA via the autoscale](https://github.com/mhausenblas/elsa#launching-elsa-through-marathon) script.


1. Stop the VM

To shut down the VM:

  ```bash
  vagrant halt
  ```
  
… or, for faster start-up but larger disk footprint:

  ```bash
  vagrant suspend
  ```

1. Destroy the VM

When you're done and want to get rid of the VM:

  ```bash
  vagrant destroy
  ```


## Kudos

Kudos to the original [Playa Mesos][5] authors:
 
* [Jeremy Lingmann](https://github.com/lingmann) ([@lingmann](https://twitter.com/lingmann))
* [Jason Dusek](https://github.com/solidsnack) ([@solidsnack](https://twitter.com/solidsnack))

VMware Support: [Fabio Rapposelli](https://github.com/frapposelli) ([@fabiorapposelli](https://twitter.com/fabiorapposelli))


[1]: http://incubator.apache.org/mesos/ "Apache Mesos"
[2]: http://github.com/mesosphere/marathon "Marathon"
[3]: http://www.virtualbox.org/ "VirtualBox"
[4]: http://www.vagrantup.com/ "Vagrant"
[5]: https://github.com/mesosphere/playa-mesos "Playa Mesos"
