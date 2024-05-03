# Team Member Names
Victoria Lawton

Sriya Kuruppath

# Instructions on how to compile/execute programs
1. Run rpi.py by typing "python3 rpi.py" into your terminal of choice. Make sure you have Conda installed and select a Conda-based interpreter to run the program.

2. The program is set to send data about Los Angeles weather and air quality every 12 seconds. Since the API we used in this project is on a free plan, the API can only be called five times every minute. Once a data point has been sent, the program will print out "Data sent to Firebase." You can check out the firebase database to confirm the data should be sent. All data should be under a node "air_quality_data" and each individual data point is under a unique key. After that, air quality data will be parsed into a .csv file, and a linear regression algorithm should interpret all of the data and print out a graph. This wouldn't be very useful if run for a short time, but if you run this for a sufficiently long time, you can see how the air quality changes in Los Angeles.

# List of any external libraries used
1. Conda

2. Pandas

3. Numpy

4. firebase_admin (from Conda)
