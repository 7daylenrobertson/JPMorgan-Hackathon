from twilio.rest import Client
import geocoder
import cv2
# test test

userName = ""
phoneNumber = 0
uses = open("uses.txt", "w")
uses.write("0")
uses.close()
counter = 0
# find a way to save this information
account_sid = "AC34a5d68ec0d37b601dce607161387a0a" # sign up with a twilio account in order to use the api, trial account
auth_token  = "39a9dcc01ff402661d311b3981ca2852"
g = geocoder.ip("me")
"""
User name is taken in the begining of the app setup and saved forever.
We would then deploy it into the actual message
same for picture
"""
def userNumber(): # return the users number
	try:
		phoneNumber = int(input("What is your number? "))
	except:
		print("Please only enter numbers\n")
		userNumber()
	if len(str(phoneNumber)) != 10:
		print("Your number must be 10 digits\n")
		userNumber()
	else:
		numberFile = open("phoneNumber.txt", "w")
		numberFile.write(str(phoneNumber))
		numberFile.close()

def firstTimeUse(): # when app is opened for the first time
	name = input("What is your full legal name? ")
	userName = open("userName.txt", "w")
	userName.write(name)
	userName.close()
	userName = open("userName.txt", "r").read()

	if len(userName) == 0:
		print("A name is required\n")
		firstTimeUse()
	else:
		print("Hello " + userName)
	userNumber()

checkUses = open("uses.txt", "r").read()
if checkUses == "0": # if this is the first time the app has been opened
	checkUses = open("uses.txt", "w")
	checkUses.write("1")
	checkUses.close()
	firstTimeUse()
	phoneNumber = open("phoneNumber.txt", "r").read()
else:
	phoneNumber = open("phoneNumber.txt", "r").read()
	userName = open("userName.txt", "r").read()

# Uses identification and token defined in 6-7 as parameters for the client
client = Client(account_sid, auth_token)

sos = client.messages.create(
	media_url = ["https://pbs.twimg.com/media/A7nSGtLCUAAq6iz.jpg"], 
	from_ = phoneNumber,
	to = "+14432533766", # change to 911 when ready
	body = ("I AM BEING HELD AGAINST MY WILL." + " MY NAME IS " + userName.upper()
	+ (". MY LATITUDE IS: " + str(g.lat)) + (". MY LONGITUDE: " + str(g.lng))
	+ (". MY CITY AND STATE IS: " + str(g)))
)

print(sos.sid)
while counter <= 5001:
	counter += 1
	if counter > 5000:
		g = geocoder.ip("me")
		print(sos.sid)

"""
Code to control camera (in order to send out pictures of surroundings every 5 minutes.
Has not been applied to main code)
Must install (pip install numpy) (pip install opencv-python) for cv2 to work
"""
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
"""
This can be used to send out to family members when 911 is texted
numbers = ["+number", "+number", "+number"]
for number in numbers:
    client.messages.create(
        #body = "Hello from my Twilio number!",
        #from_ = "+15017122662",
        #to = "number"
    )
For making calls if user isnt inside states that allow texts  Colorado, Georgia,
Illinois, Indiana, Iowa, Maine, Maryland, Montana, New York, North Carolina, Ohio,
Pennsylvania, South Carolina, Texas, Vermont, and Virginia
call = client.calls.create(
	url="http://demo.twilio.com/docs/voice.xml",
	to="+14155551212",
	from_="+15017122661"
)
print(call.sid)
"""
