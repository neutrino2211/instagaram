from InstagramAPI import InstagramAPI
import requests
import plugins

iterations = 0

class Prompt:
    def __init__(self,api):
        self.id = api.username_id
        self.api = api
        self.functions = {}
        self.descriptions = {}
        self.runtime_vars = {}
        self.function_owners = {}
    def run(self):
        r = False
        while True:
            args = self.get_args(input("> "))
            try:
                r = self.functions[args[0]](self,args[1:])
            except KeyError:
                print("Can't find '%s'"%args[0])
            except Exception as e:
                print("%s.%s crashed with error \n\n%s" % (self.function_owners[args[0]], args[0], e))
            if r:
                break

    def set_val(self,name,v):
        self.runtime_vars[name] = v

    def get_val(self,name):
        return self.runtime_vars[name]

    def load_plugin(self,plugin):
        p = plugin(self).register_functions()
        for k in p.keys():
            self.descriptions[k] = p[k]
            self.function_owners[k] = plugin.__class__.__name__
    
    def load_function(self,name,func):
        self.functions[name] = func

    def get_args(self,cmd):
        evaluate = True
        tmp = ""
        args = []
        for c in cmd:
            if c == "'":
                evaluate = not evaluate
            elif evaluate and c == " ":
                args.append(tmp)
                tmp = ""
            else:
                tmp += c
        args.append(tmp)
        return args



def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers


def printNet(a,l):
    global iterations
    if iterations < 5:
        for i in l:
            print("user:{user}, private:{private}, id:{id}".format(user=i["username"],private=i["is_private"],id=i["pk"]))
        for i in l:
            printNet(a,getTotalFollowers(a,i["pk"]))
    iterations += 1

# def get_friend_network():

def save_user_pic(f):
    profile_pic = f["profile_pic_url"]
    r = requests.get(profile_pic)
    # print(r.content)
    with open("./captures/"+str(f["pk"]+".jpg"), "wb") as f:
        f.write(r.content)

if __name__ == "__main__":
    print('''
    SOULSEARCH:
        Let's see who is out there.
    ''')
    api = InstagramAPI("neutrino2211_", "tmalamin")
    api.login()
    # print(api.username_id)
    p = Prompt(api)
    p.load_plugin(plugins.MainPlugin)
    p.run()