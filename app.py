from twitter import Twitter
import time

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
            print(len(dms))
            for i in range(len(dms)):
                message = dms[i]['message']
                sender_id = dms[i]['sender_id']
                id = dms[i]['id']

                if len(message) is not 0 and len(message) <= 500:
                    if "pkumf" in message:
                        res = [ele for ele in haramWords if(ele in message)]
                        if not res:
                            screen_name = tw.get_user_screen_name(sender_id)
                            message = message
                            tw.post_tweet(message, sender_id, screen_name)
                            tw.send_dm2(sender_id, "menfess kamu sudah terkirim! terimakasih ya wak")
                            tw.delete_dm(id)
                        else:
                            screen_name = tw.get_user_screen_name(sender_id)
                            message = message
                            errorMsg = "haram detected by "+screen_name+", msg: "+message
                            print(errorMsg)
                            tw.delete_dm(id)
                    else:
                        print("tidak sesuai trigger word")
                        tw.delete_dm(id)
            dms = list()
        else:
            print("DM is empty")
            dms = tw.read_dm()
            if len(dms) is 0:
                time.sleep(30)

if __name__ == "__main__":
    start()