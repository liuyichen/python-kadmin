python-kadmin
=============

Python module for kerberos admin (kadm5)


sample usage for pyktools.py:

>  	tools = Ktools("KISOPS.COM") # init
>   tools.authUser("user","password") # authentication
>	tools.changePassword("user","oldpassword","newpassword")	
>	admin = tools.kadmin("adminUser","password")
>	admin.listUsers() 
>	admin.delUser("user")
>	print admin.addSuperUser("user/admin","password")
>	userObject = admin.getUser("user")	
>	userObject.changePassword("newpassword")
>	userObject.lock()
>	userObject.unlock()
>	userObject.expire("2013-01-01")


sample usage for kadmin:

>  import kadmin

>  k = kadmin.init_with_keytab("user@DOMAIN", "/path/to/file.keytab")

>  p = k.get_princ("user@DOMAIN")

>  p.change_password("correcthorsebatterystaple")

>  kadmin : 
		get_principal
		list_principal
		del_principal
		add_principal
		
	principal:
		expire
		change_password

install:

请根据python版本修改该kadmin.c 的python头文件


>  #chmod 777 setup.bash

>  #./setup.bash


