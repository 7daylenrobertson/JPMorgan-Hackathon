from twilio.rest import Client
import geocoder
# You had to sign up with a twilio account in order to use the api...
#In your code. So that's what we did in line 6-7. This is our trial account
account_sid = "AC34a5d68ec0d37b601dce607161387a0a"
auth_token  = "39a9dcc01ff402661d311b3981ca2852"
g = geocoder.ip('me')
#User name is taken in the begining of the app setup and saved forever.
#We would then deploy it into the actual message
#same for picture
userName= input("Enter user full name")
counter=0

#Uses identification and token defined in 6-7 as parameters for the client
client = Client(account_sid, auth_token)

sos = client.messages.create(
    media_url=['https://pbs.twimg.com/media/A7nSGtLCUAAq6iz.jpg'], 
    from_="+18162491695",
    to="+14432533766",
    body= ("I AM BEING HELD AGAINST MY WILL."+" MY NAME IS " +userName.upper()+ (". MY LATITUDE IS: " +str(g.lat)) + (". MY LONGITUDE: " +str(g.lng))+ (". MY CITY AND STATE IS: " +str(g))))

print(sos.sid)
while counter<=30:
 counter+=1
 if counter>25:
    g = geocoder.ip('me')
    print(sos.sid)


#This can be used to send out to family members when 911 is texted
#numbers = ['+number', '+number', '+number']
#for number in numbers:
    #client.messages.create(
        #body = 'Hello from my Twilio number!',
        #from_ = '+15017122662',
        #to = 'number'
    #)
#For making calls if user isnt inside states that allow texts  Colorado, Georgia, Illinois, Indiana, Iowa, Maine, Maryland, Montana, New York, North Carolina, Ohio, Pennsylvania, South Carolina, Texas, Vermont, and Virginia
#call = client.calls.create(
 #url='http://demo.twilio.com/docs/voice.xml',
 #to='+14155551212',
 #from_='+15017122661'
#)

#print(call.sid)
