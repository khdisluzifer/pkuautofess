import tweepy
import constant
import time
import requests
from requests_oauthlib import OAuth1

class Twitter:
    def __init__(self):
        print("engine start")

    @staticmethod
    def init_tweepy():
        api = tweepy.OAuthHandler(constant.CONSUMER_KEY, constant.CONSUMER_SECRET)
        api.set_access_token(constant.ACCESS_KEY, constant.ACCESS_SECRET)
        return tweepy.API(api, wait_on_rate_limit=True)
    
    def delete_dm(self, id):
        print("Delete dm with id "+ str(id))
        try:
            api = self.init_tweepy()
            api.destroy_direct_message(id)
            time.sleep(1)
        except Exception as ex:
            print(ex)
            time.sleep(10)
            pass

    def read_dm(self):
        print("Ambil daftar DM...")
        dms = list()
        try:
            api = self.init_tweepy()
            dm = api.list_direct_messages()
            print(len(dm))
            for x in range(len(dm)):
                msg_data = dm[x].message_create['message_data']
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                gambar = ''
                try:
                    # jika dm mengandung gambar
                    if msg_data['attachment']['media']:
                        # ambil url gambar
                        gambar = msg_data['attachment']['media']['media_url']
                        # hapus url gambar dari isi tweet
                        msg_baru = message.split("https://t.co/",1)
                        # tweet tanpa url gambar
                        message = msg_baru[0]

                    else:
                        gambar = ''
                except Exception as ex:
                    pass
                if gambar != '':
                    filename = 'temp.jpg'
                    # auth untuk request gambar
                    headeroauth = OAuth1(
                        constant.CONSUMER_KEY, constant.CONSUMER_SECRET,
                        constant.ACCESS_KEY, constant.ACCESS_SECRET,
                        signature_type='auth_header'
                    )
                    # request gambar dari twitter
                    response = requests.get('%s' %gambar, auth=headeroauth)
                    print(response.status_code)
                    if response.status_code == 200:
                        with open(filename, 'wb') as image:
                            for resp in response:
                                image.write(resp)
                            print('gambar berhasil diunduh')    
                    d = dict(message = message, sender_id = sender_id, gambar = filename, id = dm[x].id)
                else:
                    d = dict(message = message, sender_id = sender_id, gambar = '', id = dm[x].id)
                dms.append(d)
                dms.reverse()
                print(str(len(dms))+" terkumpul")            
            return dms
        except Exception as ex:
            print("galat", ex)
            time.sleep(10)
            pass
    
    def post_tweet(self, msg, id, sn, gbr=''):
        print("Mengirim tweet...")
        api = self.init_tweepy()
        try:
            print("sender ", sn)
            print(msg)
            if gbr == '':
                # kirim tweet
                api.update_status(msg)
            else:
                # kirim tweet dengan gambar
                api.update_with_media(gbr,msg)
            # time.sleep(5)
        except Exception as ex:
            print(ex)
            time.sleep(10)
            pass

    def get_user_screen_name(self, id):
        print("mengambil username...")
        api = self.init_tweepy()
        user = api.get_user(id)
        return user.screen_name

    def send_dm(self, id, msg):
        print("kirim dm kalo berhasil...")
        api = self.init_tweepy()
        try:
            if api.send_direct_message(id, msg):
                print("berhasil dikirim...")
            else:
                print("tidak dikirim...")
        except Exception as ex:
            print(ex)
            time.sleep(10)
            pass