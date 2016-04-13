import os

print 'PIRATE TRADING PLATFORM uses the Robinhood retail investing service. Please enter your Robinhood credentials below.\n'

u = raw_input("Username: ")
p = raw_input("Password: ")

payload = "[['username','%s'],['password','%s']]" % (u,p)

os.system('echo "%s" > keys' % payload)