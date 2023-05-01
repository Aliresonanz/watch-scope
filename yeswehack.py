import json,requests,os.path,urllib.parse
from datetime import date
from discord import SyncWebhook

# All you need to do
# jsut set your ** Yeswehack ** webhook URL and enjoy from watch scope automation 
webhookURL = "YOUR_YESWEHACK_WEBHOOK_URL"

# the json file will create and update
path = './db/yeswehack.json'
webhook = SyncWebhook.from_url(webhookURL)
check_file = os.path.isfile(path)

try:
    if (check_file):
        # Gathering old and new data
        f = open(path)
        dataBase = json.load(f)
        x = requests.get('https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/yeswehack.json')
        data = x.json()
        f.close()

        # clear the text of json file for updating
        delete = open(path, "w")
        text = ""
        delete.write(text)
        delete.close()
        newprograms = []
        for i in range(len(data)):
            for newDomain in data[i]["scopes"]:
                newDomain2 = urllib.parse.quote(newDomain["scope"])

                # if a new program added
                if not (data[i]["thumbnail"]["name"] in dataBase):
                    if not (data[i]["thumbnail"]["name"] in newprograms):
                        newprograms.append(data[i]["thumbnail"]["name"])
                        title = "**Good news:**"
                        news = "```a new porgram added!```\n"
                        targetUrl="**Target URL:** \n"+"https://yeswehack.com/programs/"+data[i]["slug"]
                        alert = "@everyone"
                        webhook.send(title+news+targetUrl+"\n"+alert)

                # if a new scope added
                elif not (newDomain2 in dataBase[data[i]["thumbnail"]["name"]]):
                    targetName = "**Target Name:** \n{}\n".format(data[i]["title"])
                    newScope = "**new scope:** ```{}```".format(newDomain["scope"])
                    targetUrl="**Target URL:** \n"+"https://yeswehack.com/programs/"+data[i]["slug"]
                    webhook.send(newScope+"\n"+targetName+"\n"+targetUrl)
except Exception as e:
    message = "**Error in Compare process:**"
    webhook.send(message+"\n"+str(e))

# Creating or updating the json file
try:
    file = open(path,"a")
    x = requests.get('https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/yeswehack.json')
    data = x.json()
    text = '{'+'\n'
    file.write(text)
    for i in range(len(data)):
        text = '"{}":["{}"'.format(data[i]["thumbnail"]["name"],urllib.parse.quote(data[i]["title"]))
        file.write(text)
        for doamin in data[i]["scopes"]:
            text = ',"{}"'.format(urllib.parse.quote(doamin["scope"]))
            file.write(text)
        text = '],'+'\n'
        file.write(text)
    today = date.today()
    text = '"lastUpdate":"' + str(today) + '"\n}'
    file.write(text)
    file.close()
except Exception as e:
    message = "**Error in Updating process**"
    webhook.send(message+"\n"+str(e))
