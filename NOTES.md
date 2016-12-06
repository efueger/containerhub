Tasks
=====

  - tasks belong to a user
  - users get a list of notifications for tasks that are running

Network
-------

*maybe touch a file and run an hourly cron that reloads the firewall if the file is there instead of reloading it every time*

create:

  1. find next free network range
  2. copy config template to `/etc/netctl/lxcbr{{ network.id }}`
  3. activate interface
  4. update firewall rules
  5. reload firewall

delete:

  1. only continue if no running containers in the network
  2. remove ip addresses from containers
  3. deactivate bridge interface
  4. delete `/etc/netctl/lxcbr{{ network.id }}`
  5. update firewall rules
  6. reload firewall

change:

*maybe don't allow changing and use delete and add instead*

  1. only continue if no running containers in the network
  2. update network config `/etc/netctl/lxcbr{{ network.id }}`
  3. change ip addresses in db
  4. update container configs
  5. update firewall rules
  6. reload firewall

Domain
------

*maybe touch a file and run an hourly cron that reloads the lb daemon if the file is there instead of reloading it every time*

add:

  1. add domain to lb config
  2. reload lb daemon

remove:

  1. remove domain from lb config
  2. reload lb daemon

IP Address
----------

assign:

  1. only continue if container is offline
  2. update container config

Port
----

add:

  1. find next free port
  2. add forwarding to firewall config
  3. reload firewall

remove:

  1. remove port from firewall config
  2. reload firewall

Container
---------

add:

  1. create container with lxd command
  2. add ssh keys to root user
  3. Add Port forward to SSH
  4. Setup SSH inside container

remove:

  1. shutdown container if running
  2. destroy container with lxd command
  3. remove ports form container
  4. remove container from db

change:

  1. only continue if container is offline
  2. update container config

SSH Keys
--------

add:

  1. Copy key to containers users if wished

remove:

  1. Remove ssh key from containers users if wished

