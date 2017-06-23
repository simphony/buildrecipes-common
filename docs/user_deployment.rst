User deployment of EDM and simphony
-----------------------------------

This documentation defines the basics on how to setup EDM and a binary installation of simphony as an end user,
or as a developer that must build on current simphony packages. 

Please report any issue to Enthought.

What is EDM? 
-----------

EDM is a combination of a virtual environment and a dependency manager. If you
know virtualenv and pip, it's basically a combination of the two. In addition,
it supports non-python packages. It gives stricter guarantees about
functionality of the installed packages. EDM is developed by Enthought.

Installers for EDM are available at 

- https://www.enthought.com/products/edm/installers/

SimPhoNy installation
---------------------

SimPhoNy is installed by means of EDM. At the moment, only CentOS/RedHat 6 are supported.
Ubuntu will be supported soon, and should be supported for most simphony packages.

With EDM installed, you will have to perform the following steps:

- Request an API token to Enthought to access our deployment server. The token will be a random sequence 
  of characters that will be used by EDM server to authenticate your request.
- Issue the following command::

    $ edm environments create simphony 

  This will download and install a python deployment and create a virtual environment called simphony.
- edit the file ``$HOME/.edm.yaml``. Under the key repositories, add the entry::

    - enthought/simphony-dev

  as a result, the file should read as::

    repositories:
      - enthought/commercial
      - enthought/free
      - enthought/simphony-dev

- In the same file, add the auth token as::

    authentication:
        api_token: "your token in quotes"

- Save the file and issue the following command::
    
    $ edm shell --environment=simphony

  this will grant you access into the virtual environment. The prompt will reflect it by adding "(simphony)"

- Install simphony common by issuing::

    $ edm install simphony
  
  You will be prompted with a request to install the package and its dependencies. Answer Yes.

- You can now verify the presence of simphony by starting python and importing simphony::

    $ python
    >>> import simphony
    >>>


