from twitter import Twitter
import time, requests, os

tw = Twitter()
def start():
    #list of haram words
    haramWords = [
        "pantek", "p4nt3k", "p4ntek", "pant3k",
        "ngewe", "ng3w3", "ngew3", "ng3we",
        "ngentot", "ng3nt0t", "ng3ntot", "ngent0t",
        "kontol", "k0nt0l", "kont0l", "k0ntol"
        ]
    print("Starting program...")
    dms = list()
    # print(dms)
    while True:
        if len(dms) is not 0:
            # print(len(dms))
            for i in range(len(dms)):
                message = dms[i]['message']
                sender_id = dms[i]['sender_id']
                gambar = dms[i]['gambar']
                id = dms[i]['id']
                screen_name = tw.get_user_screen_name(sender_id)

                if len(message) is not 0 and len(message) <= 500:
                    if "pkumf" in message:
                        # cek apakah dm mengandung kata yang diharamkan
                        res = [ele for ele in haramWords if(ele in message)]
                        # jika dm clean...
                        if not res:                            
                            message = message
                            # jika ada gambar
                            if gambar != '':
                                # post tweet dengan gambar
                                tw.post_tweet2(message, sender_id, screen_name, gambar)
                                os.remove(gambar)
                            else:
                                tw.post_tweet(message, sender_id, screen_name)
                            tw.send_dm2(sender_id, "menfess kamu sudah terkirim! terimakasih ya wak")
                            tw.delete_dm(id)
                        else:
                            message = message
                            errorMsg = "haram detected by "+screen_name+", msg: "+message
                            print(errorMsg)
                            tw.delete_dm(id)
                    else:
                        print("tidak sesuai trigger word, sender: ", screen_name)
                        tw.delete_dm(id)
            dms = list()
        else:
            print("DM is empty")
            dms = tw.read_dm()
            if not dms:
                time.sleep(30)

if __name__ == "__main__":
    start()