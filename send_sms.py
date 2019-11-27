import os
from twilio.rest import Client
import geocoder
import cv2

userName = ""
phoneNumber = 0
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
		print("Please only enter numbers")
		userNumber()
	if len(str(phoneNumber)) != 10:
		print("Your number must be 10 digits")
		userNumber()
	else:
		return phoneNumber

def addNums2File():
	numberFile = open("textToNumbers.txt", "a")
	numbers = 0

	try:
		numbers = int(input("Enter number: "))
	except:
		print("Please only enter numbers")
		addNums2File()
	if len(str(numbers)) != 10:
		print("Your number must be 10 digits")
		addNums2File()
	else:
		numberFile.write(str(numbers) + " ")
	numberFile.close()

def otherNumbers(): # stores all emergancy numbers
	num = 0
	numberFile = open("textToNumbers.txt", "w")
	numberFile.write("912 ") # make 911 when ready
	numberFile.close()

	try:
		num = int(input("Enter how many numbers you want to text incase of emergcy: "))
	except:
		print("Enter only numbers")
		otherNumbers()

	for i in range(0, num):
		addNums2File()

	help = input("Do you need help right now? Y/N ")
	if help.upper() == "Y":
		call4Help(g)
	else:
		print("Okay, stay safe!")

def firstTimeUse(): # when app is opened for the first time
	name = input("What is your full legal name? ")
	userName = open("userName.txt", "w")
	userName.write(name)
	userName.close()
	userName = open("userName.txt", "r").read()

	if len(userName) == 0:
		print("A name is required")
		firstTimeUse()
	else:
		print("Hello " + userName)

	phoneNumber = userNumber()
	numberFile = open("phoneNumber.txt", "w")
	numberFile.write(str(phoneNumber)) # store user number
	numberFile.close()

	question = input("Do you have any other numbers you would like to input? Y/N ")
	if question.upper() == "Y":
		otherNumbers()
	else:
		numberFile = open("textToNumbers.txt", "w")
		numberFile.write("912 ") # make 911 when ready
		numberFile.close()

	uses = open("uses.txt", "w") # app knows that it has been set up
	uses.write("1")
	uses.close()

def call4Help(g):
	# Uses identification and token defined in 6-7 as parameters for the client
	client = Client(account_sid, auth_token)
	phoneNumber = open("phoneNumber.txt", "r").read()
	numberFile = open("textToNumbers.txt", "r").read()
	cnt = 0

	for i in range(0, len(numberFile)): # count how many phone numbers
		if numberFile[i] == " ":
			cnt += 1

	lstNum = [""]*cnt
	j = 0

	for i in range(0, len(numberFile)): # adds numbers to list
		if numberFile[i] != " ":
			lstNum[j] += numberFile[i]
		else:
			j += 1

	for i in range(0, len(lstNum)): # text all emergncy contact
		sos = client.messages.create(
			media_url = ["https://pbs.twimg.com/media/A7nSGtLCUAAq6iz.jpg"],
			from_ = phoneNumber,
			to = lstNum[i],
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

if os.path.exists("uses.txt"): # determin if app has been set up
	uses = open("uses.txt", "r").read()
	if uses == "0":
		firstTimeUse()
	else:
		help = input("Do you need help? Y/N ")
		if help.upper() == "Y":
			call4Help(g)
		else:
			print("Okay, stay safe!")
else:
	uses = open("uses.txt", "w")
	uses.write("0")
	uses.close()
	firstTimeUse()

"""
Code to control camera (in order to send out pictures of surroundings every 5 minutes.
Has not been applied to main code)
Must install (pip install numpy) (pip install opencv-python) for cv2 to work
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

This can be used to send out to family members when 911 is texted
Already handled in call4Help function
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
