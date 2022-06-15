# user credentials to access the cisco


from ncclient import manager
RTR1_MGR = manager.connect(host= "ios-xe-mgmt.cisco.com",
                           port = 830,
                           username = "developer",
                           password = "C1sco12345",
                           hostkey_verify = False)


from flask import Flask


# Creating the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.get('/GetConfig')
# create a main() method

def main():
    """Main method that configures the Ip address for a interface via NETCONF."""

    # Show command that we need to execute
    command = "show ip int brief"
    config_details = SendCommandToDevice(command)
    if config_details == 0:
        return "error in the function"
    else:
        return config_details



# this statement performs a Create Loopback on the specified url

@app.post('/Create_Loopback')
def create_looback():


    creation_rpc = '''
    <config>
       <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">     
        <interface>
                <Loopback>
          <name>2</name>
          <ip>
            <address>
              <primary>
                <address>10.10.10.10</address>
                <mask>255.255.255.255</mask>
              </primary>
            </address>
          </ip>
        </Loopback>
      </interface>
    </native>
</config>
'''

    send_return = sendmanager(creation_rpc)

    if send_return == 0:
        return "Error in the function"
    else:
        return "Created the interface"


# Function to send the required interface level details to the device using connect manager

def sendmanager(rpc_msg):

    with manager.connect(host="ios-xe-mgmt.cisco.com",
                         port=830, username='developer',
                         password='C1sco12345',
                         hostkey_verify=False) as m:

     reply = m.edit_config(rpc_msg , target='running')

def SendCommandToDevice(command):
    from netmiko import ConnectHandler

# credentials to access the cisco

    cisco1 = {
        "device_type": "cisco_xe",
        "host": "ios-xe-mgmt.cisco.com",
        "username": "developer",
        "password": "C1sco12345",
    }

    with ConnectHandler(**cisco1) as net_connect:
        output = net_connect.send_command(command)

    # Automatically cleans-up the output so that only the show output is returned
    return output


# this statement performs a DELETE on the specified url

@app.post('/Delete_loopback')

# function used to get the configurations of a device
def Delete_loopback():

    rpc_message = '''
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">     
       <interface>              
       <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
              <name>3</name>
              </Loopback>
          </interface>
        </native>
    </config>
    '''
    send_return = sendmanager(rpc_message)

    if send_return == 0:
        return "Error in the function"
    else:
        return "deleted the interface"



# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
    
