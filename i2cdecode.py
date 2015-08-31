import pyvisa

rm = pyvisa.ResourceManager()

try:
	mso = rm.open_resource('TCPIP::192.168.1.148::INSTR')
	print("Connected to " + mso.query("*idn?"))
except:
	print("Couldn't connect.")
	exit(1)

# Reset scope
mso.write("*rst")
mso.write("*clr")

# Configure the display graph
mso.write('acq:state off') # Stop acq
mso.write("sel:ch2 on") # Turn CH2 on
mso.write("autoset execute") # Autoset display
mso.write("ch2:pos 0") # Set CH2's vertical position to 0
mso.write("hor:mode manual")
mso.write("hor:mode:scale 200e-6") # Setting the horizontal scale to 200 microseconds
mso.write("hor:mode:recordlength 100000")
print("Configured display graph")

# Configure bus1
mso.write("bus:b1:type i2c") # Setting bus 1 to decode I2C
mso.write("bus:b1:i2c:data:source ch2") # Bus 1 will look at CH2 for data
mso.write("bus:b1:pos -2") # Setting the bus decode data below the x-axis
mso.write("sel:b1 on") # Turn on bus 1
print("Configured bus 1 to I2C")

# Configure the trigger
mso.write("trig:a:bus:i2c:cond start") # Trigger on a "Start" packet for I2C
mso.write("acq:stopafter seq")
mso.write("acq:state on")
mso.write("*wai") # Wait for the scope to finish processing before saving the file
mso.write("SAVE:EVENTTABLE:BUS1 \"C:\\Users\\Tek_Local_Admin\\Desktop\\BusDecode\"")
print("Saved results to a file.")

input("Press enter to quit.")
