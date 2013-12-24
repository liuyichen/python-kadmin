# -*- coding:utf-8 -*-
"""
class Ktools
	用于 kerberos 操作 及 管理

requires libraries: 
	kerberos : 
		checkPassword
		changePassword
	kadmin : 
		get_principal
		list_principal
		del_principal
		add_principal
		
	  principal:
		  expire
		  change_password
		
"""
import kerberos
import kadmin
import re
from time import time
from datetime import datetime
" timeout sec"
EXPIRE = 86400*24*90

class Ktools(object):

	def __init__(self,daemon):
		self.daemon = daemon
		
	def authUser(self,user,password):
		return kerberos.checkPassword(user,password,"",self.daemon)

	def changePassword(self,user,old,new):
		return kerberos.changePassword(user,old,new)

	def kadmin(self,user,password):
		" init kadmin object by admin user and password "
		if not re.search("/admin$",user):
			raise kadmin.KAdminError , "User %s is not AdminUser."%user
		return Kadmin(user,self.daemon,password)

class Kadmin(object):
	
	def __init__(self,user,daemon,password):
		self.daemon = daemon
		adminUser = "%s@%s"%(user,self.daemon)
		self.admin = kadmin.init_with_password(adminUser,password)
	
	def changePassword(self,user,password):
		return user.changePassword(password)
	
	def getUser(self,userName):
		return Kuser(self.admin,userName)

	def listUsers(self,):
		return list( self.yieldUsers() )

	def yieldUsers(self,):
		for u in self.admin.list_principals():
			u = re.findall(r"(.*?)@%s$"%self.daemon,u)[0]
			yield u

	def delUser(self,userName):
		return self.admin.del_principal(userName)

	def addUser(self,userName,password):
		if re.search("/",userName):
			raise kadmin.KAdminError,"Failed userName format by '/'."
		return self.admin.create_principal(userName,password)

	def addSuperUser(self,userName,password):
		if not re.search("/admin$",userName):
			raise kadmin.KAdminError,"UserName format need '%s/admin'."
		return self.admin.create_principal(userName,password)

    def addAppUser(self,userName,host,password):
        pass                

class Kuser(object):

	"""
		extends method
			: expire 
	"""
	
	def __init__(self,admin,userName):
		self.admin = admin
		self.user = admin.get_principal(userName)

	def changePassword(self,password):
		return self.user.change_password(password)
	
	def lock(self,):
		return self.user.expire("")

	def unlock(self,):
		" add some days by now()"
		expireDatetime = datetime.fromtimestamp(time()+EXPIRE).__str__()
		return self.user.expire(expireDatetime)

	def __getattr__(self,key):
		" extends kadmin principal object method "
		return getattr(self.user,key)

if __name__ == "__main__":
	" debug testing "
	tools = Ktools("KISOPS.COM")
	retval = tools.authUser("root/admin","11qq```")
	print " auth root/admin by password result : %s "% retval
	retval = tools.changePassword("root/admin","11qq```","11qq```")	
	admin = tools.kadmin("root/admin","11qq```")
	print admin.listUsers()
	print admin.delUser("liuyc/admin")
	print admin.addSuperUser("liuyc/admin","321321")
	u = admin.getUser("liuyc/admin")	
	print u.changePassword("321321")
	print u.lock()
	print u.unlock()
	print u.expire("2013-01-01")


