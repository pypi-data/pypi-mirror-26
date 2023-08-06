# lockboxcli
command line for lockbox

# example usage
from lockboxcli import LockboxClient
client = LockboxClient('staging')

pip_test = client.get_secret('PIP_TEST')
print(pip_test)

client.update_secret('PIP_TEST', 'bazquux')

pip_test = client.get_secret('PIP_TEST')
print(pip_test)
