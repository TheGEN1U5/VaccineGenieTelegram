import requests
from telegram.ext import Updater, CommandHandler
import datetime

# district dat collection
districtId = []
for i in range(37):
    query = i+1
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(query)
    params = {
        "state_id": query
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()['districts']
    for district in data:
        districtId.append(district)


def nameToId(dName):
    for district in districtId:
        if dName.lower() == district['district_name'].lower():
            return district['district_id']
# Telegram Integration


def start(update, context):
    instructions = '''
    Use /find <district name> to find available slots in your district for the age group 18-44 \n
    For regular and instant updates on vaccine slots join https://t.me/joinchat/6DNtwlDkbL5jMTY9 \n
    
    Bot by GEN1U5
    '''
    update.message.reply_text(instructions)
    

def find(update, context):
    query = update.message['text'].replace('/find ', '')
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
    if nameToId(query) != None:
        params = {
            "district_id": nameToId(query),
            "date": datetime.date.today().strftime('%d-%m-%y')
        }

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
        resp = requests.get(url, params=params, headers=headers)
        data = resp.json()
        sessions = data['sessions']

        availableCenters = []

        for session in sessions:
            if session['min_age_limit'] == 18:
                availableCenters.append(session)

        if len(availableCenters) > 0:
            print(len(availableCenters))
            for center in availableCenters:
                messg = f"VACCINES AVAILABLE \n {center['pincode']} \n {center['date']} \n {center['district_name']} \n {center['name']} \n {center['available_capacity']} of {center['vaccine']} for 18+ \n Dose 1: {center['available_capacity_dose1']} slot(s) \n Dose 2: {center['available_capacity_dose2']} slot(s) \n \n Made by GEN1U5"
                update.message.reply_text(messg)
        else:
            update.message.reply_text('No Vaccine available in this district for the age group 18-44 yet. Keep Checking...')
    else:
        update.message.reply_text(f'No district found with name \"{query}\"')



def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1841864143:AAHU2VlHgO-S1OzZtYGLHzLu8VVkeQQrKl8", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("find", find))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

main()


