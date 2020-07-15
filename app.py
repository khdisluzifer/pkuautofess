from twitter import Twitter
import time

tw = Twitter()
def start():
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
                        screen_name = tw.get_user_screen_name(sender_id)
                        message = message
                        tw.post_tweet(message, sender_id, screen_name)
                        tw.delete_dm(id)
                    # else:
                        # tw.send_dm(sender_id)
            dms = list()
        else:
            print("DM is empty")
            dms = tw.read_dm()
            if len(dms) is 0:
                time.sleep(30)

if __name__ == "__main__":
    start()