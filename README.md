c-base-playground
=================

Your linux container is just one click away!

FAQ
===

Accounts
--------

Everybody can register an account. To actually use the functionality provided by the playground you need to
verify your c-base membership. At the moment this is done by authenticating against the c-base ldap with your member
name and password. In future versions this will be replaced by OAuth2 or something better but it's not ready yet.
These infos are not stored on the server and only used to get your membership status.
If you cancel your c-base membership you will not be able to generate new containers but your existing ones will
continue to work.

Due to technical limitations there will be a maximum of 255 accounts on the server. If more accounts are needed a seperate server will be put in place.

Container
---------

Users can create as many linux containers as they want. This could change in future updates if technical barriers are reached.

Networks
--------

One Users containers will be on the same network so you can setup more complex systems if you want. Connections between User networks are not planned as of now but could be added with a future update.

IP Addresses
------------

The host system has only one IPv4 address under which your containers will be accessable. Your containers will get a
IPv6 subnet and an internal IPv4 subnet from where you can assign IP addresses to your containers.

Ports
-----

You can request ports that will be forwarded to your containers. At the moment there is no maximum in how many ports you
can request. A maximum will be set when this feature is abused by a user or when the host runs out of free ports.

Once an hour forwarded ports to the containers will be added and removed.

Domains
-------

You can attach a domain to one of your containers. All incomging HTTP and HTTPS requests will be forwarded to the container you
selected.

SSL Certificates
----------------

After you set up your domains, you can easily aquire SSL certificates from [Letsencrypt][letsencrypt].


[letsencrypt]: https://letsencrypt.org/
