import tweepy
import constant
import time
import requests
from requests_oauthlib import OAuth1

class Twitter:
    def __init__(self):
        print("init twitter api")

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
            # print(len(dm))
            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                gambar = dm[x].message_create['message_data']['attachment']['media']['media_url']
                if gambar != '':
                    filename = 'temp.jpg'
                    # print(gambar)
                    headeroauth = OAuth1(constant.CONSUMER_KEY, constant.CONSUMER_SECRET,
                     constant.ACCESS_KEY, constant.ACCESS_SECRET,
                     signature_type='auth_header')
                    # authe = tweepy.OAuthHandler(constant.CONSUMER_KEY, constant.CONSUMER_SECRET)
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
            print("tes")
            time.sleep(5)
            return dms

        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass
    
    def post_tweet(self, msg, id, sn):
        print("Mengirim tweet...")
        api = self.init_tweepy()
        try:
            print("sender ", sn)
            print(msg)
            api.update_status(msg)
            time.sleep(5)
        except Exception as ex:
            # api.destroy_direct_message(id)
            # api.send_direct_message(id, "kirim menfess kamu dalam jangka waktu 15 menit untuk menghindari duplikasi")
            print(ex)
            time.sleep(60)
            pass
    
    def post_tweet2(self, msg, id, sn, gbr):
        print("Mengirim tweet...")
        api = self.init_tweepy()
        try:
            print("sender ", sn)
            print(msg)
            api.update_with_media(gbr,msg)
            time.sleep(5)
        except Exception as ex:
            # api.destroy_direct_message(id)
            # api.send_direct_message(id, "kirim menfess kamu dalam jangka waktu 15 menit untuk menghindari duplikasi")
            print(ex)
            time.sleep(60)
            pass


    def get_user_screen_name(self, id):
        print("mengambil username...")
        api = self.init_tweepy()
        user = api.get_user(id)
        return user.screen_name

    def send_dm(self, id):
        print("membalas pesan, tidak sesuai trigger")
        api = self.init_tweepy()
        try:
            #api.send_direct_message(id, "trigger word tidak sesuai. gunakan rzmf untuk mengirim menfess!")
            api.destroy_direct_message(id)
        except Exception as ex:
            # api.send_direct_message(id, "kirim menfess kamu dalam jangka waktu 15 menit untuk menghindari duplikasi")
            print(ex)
            time.sleep(60)
            pass
    
    def send_dm2(self, id, msg):
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