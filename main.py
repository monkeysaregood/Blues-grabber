import discum, threading, yaml, os, asyncio, random, base64, time, sys, threading, requests
from api.database import Manager
from api.colors import colors

os.system('cls'); print("Iniciando ...")

try: 

    with open('config/settings.yaml', encoding='utf-8') as f:
        
        settings = yaml.load(f, Loader=yaml.FullLoader)
        settings['_'] = "hakeatos"
        f.close()

    with open('config/message.txt', encoding='utf-8') as f:

        settings['message'] = f.read()
        f.close()

    if settings['mask_link']:
        for line in settings['message'].split():
            if "https://discord.gg/" in line:
                new_link = settings['mask']
                new_message = settings['message'].replace(line, f"<{new_link}> ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _ {line}")
                settings['message'] = new_message

    tokens = sys.argv
    tokens.remove(tokens[0])
    if len(tokens) == 0: tokens = open('config/tokens.txt').read().splitlines()
    tokens_index = {}

    for token in tokens: tokens_index[token] = {'is_sleeping': False, 'is_rate_limit': False, 'sleep_10_minutes':0, 'reply_users_sience' : {}}

    db = Manager(settings['mongo_db_url'])

except Exception as e:
    print(f'Erro: {e}')

class stats:

    dms_deliver = 0
    dms_captured = 0
    dms_sends = []

class instance(object):

    def __init__(self, db, settings) -> None:

         self._ = settings['_']
         self.db = db 
         self.token = settings['token']
         self.settings = settings
         self.message = settings['message']
         self.cookies = False 

    def check_user(self, userid):

        if self.db.store_user_data(self._, self.settings["mongo_cluster_name"], str(userid)):
            return True
        else:
            return False


    def add_user(self, userid):

        if self.db.insert_user_data(self._, self.settings["mongo_cluster_name"], str(userid)):
            return True 
        else:
            return False

def sience_to_dm(bot, nav, user):
    global tokens_index
    if not tokens_index[bot._Client__user_token]['is_sleeping'] and not "bot" in user:                        
                        if "guild_id" in user:
                            if not nav.check_user(user['id']):
                                if nav.add_user(user['id']):
                                    tokens_index[bot._Client__user_token]['is_sleeping'] = True
                                    if int(tokens_index[bot._Client__user_token]['sleep_10_minutes']) == 10:
                                     print(f'{colors.GREY}[{colors.CYAN}*{colors.GREY}]{colors.RESET} {get_id(bot._Client__user_token)} {colors.GREY}| {colors.CYAN}Aguardando 5 minutos{colors.RESET}{colors.RESET}.')
                                     tokens_index[bot._Client__user_token]['sleep_10_minutes'] = 0
                                     time.sleep(100)
                                     print(f'{colors.GREY}[{colors.GREEN}+{colors.GREY}]{colors.RESET} {get_id(bot._Client__user_token)} {colors.GREY}| {colors.GREEN}Aguardado 5 minutos{colors.RESET}{colors.RESET}.')
                                    try:
                                     newDM = bot.createDM([user['id']]).json()["id"]
                                    except:
                                       print(f'{colors.GREY}[{colors.RED}!{colors.GREY}]{colors.RESET} {get_id(bot._Client__user_token)} {colors.GREY}|{colors.RED} Caiu para verificação.')
                                       return bot.gateway.close()
                                    r = bot.gateway.request.call(newDM, video=True)
                                    bot.typingAction(newDM)
                                    stats.dms_captured += 1
                                    tokens_index[bot._Client__user_token]['sleep_10_minutes'] += 1
                                    try:
                                     guild = bot.gateway.session.guild(user["guild_id"]).name
                                    except:
                                     guild = None
                                    print(f'{colors.GREY}[{colors.BLUE}*{colors.GREY}]{colors.RESET} {get_id(bot._Client__user_token)} {colors.GREY}|{colors.BLUE} ({tokens_index[bot._Client__user_token]["sleep_10_minutes"]}/10) Capturado{colors.RESET}: {colors.CYELLOW}{user["username"]}{colors.RESET}. {colors.BLUE}Servidor{colors.RESET}: {colors.CYELLOW}{guild}')
                                    _thread = threading.Thread(target=between_callback, args=(bot._Client__user_token,))
                                    _thread.start()

    if not "guild_id" in user:
                         
                         newDM = user['channel_id']
                         if not user['id'] == get_id(bot._Client__user_token) and not user['id'] in stats.dms_sends: 
                          stats.dms_sends.append(user['id'])
                          if settings['dm_typing']: bot.typingAction(newDM)
                          if settings['dm_reaction']: bot.addReaction(newDM, user['message_id'], get_emoji())
                          if settings['dm_reply']: bot.reply(newDM, user['message_id'], settings['message'])
                          else: bot.sendMessage(newDM, settings['message'])
                          if settings['dm_pin']: bot.pinMessage(newDM, user['message_id'])
                          stats.dms_deliver+=1
                          
                          print(f'{colors.GREY}[{colors.GREEN}+{colors.GREY}]{colors.RESET} {get_id(bot._Client__user_token)} {colors.GREY}| {colors.GREEN}Mensagem enviada{colors.RESET}: {colors.CYELLOW}{user["username"]}{colors.RESET}.')
                          tokens_index[token]['reply_users_sience'][user['id']] = []

                         elif not user['id'] == get_id(bot._Client__user_token) and user['id'] in stats.dms_sends:
                            bot.addReaction(newDM, user['message_id'], get_emoji())
                            for msg in settings['reply_messages']:
                             if not user['id'] in tokens_index[token]['reply_users_sience']: tokens_index[token]['reply_users_sience'][user['id']] = []
                             if not msg in tokens_index[token]['reply_users_sience'][user['id']]:
                                bot.typingAction(newDM)
                                time.sleep(random.randint(1, 2))
                                bot.reply(newDM, user['message_id'], msg)
                                tokens_index[token]['reply_users_sience'][user['id']].append(msg)
                                #bot.sendMessage(newDM, msg)
                                break




    
def get_start_banner():
 start_banner = f'''{colors.CYAN} 
  ____       _  __   _           _   
 / ___|  ___| |/ _| | |__   ___ | |_ 
 \___ \ / _ \ | |_  | '_ \ / _ \| __|
  ___) |  __/ |  _| | |_) | (_) | |_ 
 |____/ \___|_|_|   |_.__/ \___/ \__|
                                     
{colors.RESET}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{colors.CYAN} Tempo de espera{colors.RESET}: {settings["dm_cooldown"]} segundos
{colors.CYAN} Total de tokens{colors.RESET}: {len(tokens)}
{colors.RESET}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'''
 return start_banner

def get_emoji():
    return random.choice(settings['reactions'])


def update_title(guilds=None):
    os.system(f'title LuKas Selfbot [Enviados {stats.dms_deliver}, Capturados {stats.dms_captured}, Multi-tokens {len(tokens)}, Servidores {guilds}]')

async def reset_sleep(token):
 if settings["dm_cooldown"] > 0:
        await asyncio.sleep(settings['dm_cooldown']); tokens_index[token]['is_sleeping'] = False
         
async def some_callback(token):
    await reset_sleep(token)

def between_callback(token):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(some_callback(token))
    loop.close() 

def get_id(token):

        id = token.split(".")[0]
        id += "=" * ((4 - len(id) % 4) % 4)
        id = base64.b64decode(id).decode('ascii')
        return id

def get_token_guilds(token):
    headers = {
    'authority': 'discord.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,mn;q=0.6',
    'authorization': token,
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '__dcfduid=9d2e50d43e0a11ed8a17e636b754be3a; __sdcfduid=9d2e50d43e0a11ed8a17e636b754be3a1b3a70b875bfee7709c9f86dc78a03f4ef43932d74295664edd061beff1bb9a7; _ga=GA1.2.241072284.1664977992; OptanonConsent=isIABGlobal=false&datestamp=Wed+Oct+05+2022+11%3A29%3A52+GMT-0300+(Brasilia+Standard+Time)&version=6.33.0&hosts=&consentId=f1f1ee1f-88df-44ae-af2e-15e379ffd247&interactionCount=1&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0; __stripe_mid=442d4cbc-481c-4363-b564-d5b04d217b5e1152b0; __cfruid=0e0eb28533d661290032b855b45d5080ecfb0227-1666737614; locale=ro; __cf_bm=Uv0qicvCGyjWIzTMnVmwFvsFfjOMZD_n4FVF_ankIcI-1666740905-0-ATJ/Ewr3nZImoseRDddrvQbGcGtsnSr3nZ0ONaXiGNivcRaImH7BUGWr3oi+Y19/mSye2oah4SBaCl1DZR5LKOcGR5RHBq1fVDW9ZHVVJInXmHuIO46i/3hbWA6Ogeiuow==',
    'pragma': 'no-cache',
    'referer': 'https://discord.com/channels/@me',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'ro',
    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tL2NoYW5uZWxzL0BtZSIsInJlZmVycmluZ19kb21haW4iOiJkaXNjb3JkLmNvbSIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxNTQxODYsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
}

    response = requests.get('https://discord.com/api/v10/users/@me/guilds', headers=headers)
    return response.json()

def start_discord(tokenlist):

        def AfterReadySupp(resp, bot):
            if resp.event.ready_supplemental:
                        #update_title(len(bot.getGuilds().json())) 
                        try:
                         guilds = []
                         r = get_token_guilds(bot._Client__user_token)
                         for g in r:
                            guilds.append(g['id'])
                         bot.gateway.subscribeToGuildEvents(wait=1, guildIDs=guilds, token=bot._Client__user_token)
                        except:
                             print(f'{colors.GREY}[{colors.RED}!{colors.GREY}] {colors.RESET}{get_id(bot._Client__user_token)} {colors.GREY}| Não foi possivel completar as configurações nos eventos dos servidores, talvez em algumas guildas essa conta não funcionará.') 
                        
                        print(f'{colors.GREY}[{colors.GREEN}!{colors.GREY}] {colors.RESET}{get_id(bot._Client__user_token)} {colors.GREY}| Cliente {colors.GREEN}conectado{colors.GREY} e escutando eventos em {colors.RESET}{len(bot.getGuilds().json())} {colors.GREY}servidores.')
                        try:
                         bot.setProfileColor('red')
                         bot.enableDevMode(True)
                         bot.gateway.setStatus("idle")
                         bot.gateway.setCustomStatus("https://discord.gg/night-bar")
                        except:
                            pass
        clients = []
        for i in range(len(tokenlist)):
            if i == 0:
                clients.append(discum.Client(token=tokenlist[0], log=False))
            else:
                newBot = discum.Client(token=tokenlist[i], log=False)
                newBot.s.cookies.update(clients[0].s.cookies)
                clients.append(newBot)
            clients[i].gateway.command({"function": AfterReadySupp, "params":{"bot":clients[i]}})



        def gatewayRunner(bot, result, index):

            nav_settings = settings
            nav_settings["token"] = bot._Client__user_token
            nav = instance(db, nav_settings)

            @bot.gateway.command
            def callTest(resp):
        
                if resp.event.message:
                 if settings['event_message']:
                    m = resp.parsed.auto()
                    user = m['author']
                    if "guild_id" in m:
                     user['guild_id'] = m['guild_id']
                    if "channel_id" in m:
                     user['channel_id'] = m['channel_id']
                    if "id" in m:
                     user['message_id'] = m['id']
                    if "content" in m:
                     user['content'] = m['content']
                    if "bot" in m:
                     user['bot'] = m['bot']

                
                    sience_to_dm(bot, nav, user)

                elif resp.event.voice_state_updated:
                  if settings['event_voice']:
                    m = resp.parsed.auto()
                    if 'member' in m:
                        user = m['member']['user']
                        if "guild_id" in m:
                         user['guild_id'] = m['guild_id']                                               
                        if "channel_id" in m:
                         user['channel_id'] = m['channel_id']
                        if "id" in m:
                         user['message_id'] = m['id']
                        if "content" in m:
                         user['content'] = m['content']   
                        if "bot" in m:
                         user['bot'] = m['bot']
                  
                        sience_to_dm(bot, nav, user)
                                    
                update_title()          
                
            
            bot.gateway.run(auto_reconnect=True)
            
            result[index] = bot.gateway.session.user
            
        os.system('cls'); print(get_start_banner())
        num_clients = len(clients)
        threads = [None] * num_clients
        results = [None] * num_clients

        for i in range(num_clients):
            threads[i] = threading.Thread(target=gatewayRunner, args=(clients[i] , results, i))  # type: ignore
            threads[i].start() # type: ignore


start_discord(tokens); input()

