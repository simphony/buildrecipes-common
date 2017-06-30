provision: edm openmpi

edm:
	sudo yum install -y https://package-data.enthought.com/edm/rh5_x86_64/1.7/edm_1.7.0_x86_64.rpm

openmpi:
	sudo yum install -y openmpi openmpi-devel 

openfoam:
	sudo yum groupinstall 'Development Tools'
	sudo yum install openmpi openmpi-devel qt zlib-devel cmake
	sudo yum-config-manager --nogpgcheck --add-repo http://dl.atrpms.net/el6-x86_64/atrpms/stable
	sudo yum install --nogpgcheck qtwebkit qtwebkit-devel
	sudo yum install --nogpgcheck CGAL CGAL-devel
	sudo rpm -i --force https://www.openfoam.org/download/rhel/6.5/x86_64/OpenFOAM-scotch-6.0.0-1.x86_64.rpm
	sudo rpm -i --force https://www.openfoam.org/download/rhel/6.5/x86_64/OpenFOAM-ParaView-3.12.0-1.x86_64.rpm
	sudo rpm -i --force https://www.openfoam.org/download/rhel/6.5/x86_64/OpenFOAM-2.3.0-1.x86_64.rpm	
