# ElSA to-go

ElSA to-go is derived from [Playa Mesos][1] which in turn relies on [VirtualBox][2] and [Vagrant][3], and an Ubuntu box image.

## Prerequisites

* [VirtualBox][2] 4.2+
* [Vagrant][3] 1.3+

## Quick Start

Preparation:

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

Once you're done experimenting, you can shut down the VM like so:

  ```bash
  vagrant halt
  ```
  
… or, for faster start-up but larger disk footprint:

  ```bash
  vagrant suspend
  ```

When you want to get rid of the VM, do the following:

  ```bash
  vagrant destroy
  ```


## Kudos

Kudos to the original [Playa Mesos][1] authors:
 
* [Jeremy Lingmann](https://github.com/lingmann) ([@lingmann](https://twitter.com/lingmann))
* [Jason Dusek](https://github.com/solidsnack) ([@solidsnack](https://twitter.com/solidsnack))

[1]: https://github.com/mesosphere/playa-mesos "Playa Mesos"
[2]: http://www.virtualbox.org/ "VirtualBox"
[3]: http://www.vagrantup.com/ "Vagrant"
