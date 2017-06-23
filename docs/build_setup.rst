Build machine setup
-------------------

The build machine is a redhat CentOS 6. The runtime must be setup with appropriate dependencies, for which the
provided makefile takes care. This operation must be performed only once, if a new virtual machine is needed. 
It may, however, be modified (and the associated rule performed) if new "apt level" packages are required.
For example, if a new simphony or force package requires libpng installed via apt, the makefile should be changed
to accommodate that.

Login on the build machine as root, and perform the operation::

    make provision

This provisions the build machine with the required dependencies for the build.
