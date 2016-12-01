c-base-playground
=================

Your linux container is just one click away!

FAQ
===

Account
-------

Everybody on the internet can register an account. To use the functionality provided by the playground you need to
verify your c-base membership. At the moment this is done by authenticating against the c-base ldap with your member
name and password. In future versions this will be replaced by OAuth2 or something better but it's not ready yet.
These infos are not stored on the server and only used to get your membership status.
If you cancel your c-base membership you will not be able to generate new containers but your existing ones will
continue to work.

Container
---------

Verified c-base users can create as many linux containers as they want.

IP Addresses
------------

The host system has only one IPv4 address under which your container will be accessable. Your containers will get a
IPv6 subnet where you can setup any configuration you want.

Ports
-----

You gen request ports that will be forwarded to your container. At the moment there is no maximum in how many ports you
can request. A maximum will be set when this feature is abused by a user.

Once an hour forwarded ports to the containers will be added and removed.

Domains
-------

You can attach an extenral domain to one of your containers. All incomging HTTP and HTTPS requests will be forwarded to the container you
selected.

SSL Certificates
----------------

After you set up your domains easily aquire SSL certificates from Letsencrypt.

