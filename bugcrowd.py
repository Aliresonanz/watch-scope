import json,requests,os.path,urllib.parse
from datetime import date
from discord import SyncWebhook

# All you need to do
# jsut set your ** Bugcrowd ** webhook URL and enjoy from watch scope automation 
webhookURL = "YOUR_BUGCROWD_WEBHOOK_URL"

# the json file will create and update
path = './db/bugcrowd.json'
webhook = SyncWebhook.from_url(webhookURL)
check_file = os.path.isfile(path)

try:
    if (check_file):
        # Gathering old and new data
        f = open(path)
        dataBase = json.load(f)
        x = requests.get('https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/bugcrowd.json')
        data = x.json()
        f.close()

        # clear the text of json file for updating
        delete = open(path, "w")
        text = ""
        delete.write(text)
        delete.close()
        newprograms = []
        for i in range(len(data)):
            for group in data[i]["target_groups"]:
                for newDomain in group["targets"]:
                    newDomain2 = urllib.parse.quote(newDomain["name"])

                    # if a new program added
                    if not (data[i]["code"] in dataBase):
                        if not (data[i]["code"] in newprograms):
                            newprograms.append(data[i]["code"])
                            title = "**Good news:**"
                            news = "```a new porgram added!```\n"
                            targetUrl="**Target URL:** \n"+"https://bugcrowd.com"+data[i]["program_url"]
                            alert = "@everyone"
                            webhook.send(title+news+targetUrl+"\n"+alert)

                    # if a new scope added
                    elif not (newDomain2 in dataBase[urllib.parse.quote(data[i]["code"])]):
                        targetName = "**Target Name:** \n{}\n".format(data[i]["name"])
                        targetGroup = "**Group Name:** \n{}\n".format(group["name"])
                        newScope = "**new scope:** ```{}```".format(newDomain["name"])
                        targetUrl="**Target URL:** \n"+"https://bugcrowd.com"+data[i]["program_url"]
                        webhook.send(newScope+"\n"+targetName+"\n"+targetGroup+"\n"+targetUrl)
except Exception as e:
    message = "**Error in Compare process:**"
    webhook.send(message+"\n"+str(e))

# Creating or updating the json file
try:
    file = open(path,"a")
    x = requests.get('https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/bugcrowd.json')
    data = x.json()
    text = '{'+'\n'
    file.write(text)
    for i in range(len(data)):
        text = '"{}":["{}"'.format(urllib.parse.quote(data[i]["code"]),urllib.parse.quote(data[i]["name"]))
        file.write(text)
        for group in data[i]["target_groups"]:
            for domain in group["targets"]:
                text = ',"{}"'.format(urllib.parse.quote(domain["name"]))
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
