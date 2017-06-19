provision: edm openmpi

edm:
	sudo yum install -y https://package-data.enthought.com/edm/rh5_x86_64/1.7/edm_1.7.0_x86_64.rpm

openmpi:
	sudo yum install -y openmpi openmpi-devel 
