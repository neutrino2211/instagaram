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

class MainPlugin:
    def __init__(self,prompt):
        self.prompt = prompt

    def register_functions(self):
        self.prompt.load_function("followers",self.get_followers)
        self.prompt.load_function("exit",self.exit_)
        self.prompt.load_function("help",self.help)
        self.prompt.load_function("following",self.get_following)
        return {
            "help": "print all commands and their descriptions",
            "exit": "Quit the prompt",
            "followers": "Get followers for user id given in the first argument or none to get your followers",
            "following": "Get people following the user id given or your followings"
        }

    def help(self,p,a):
        for k in p.functions.keys():
            print(k+" : "+p.descriptions[k])

    def get_followers(self,prompt,args):
        followers = getTotalFollowers(prompt.api,args[0] if len(args) > 0 else prompt.id)
        string = "\n\t"+"\n\t".join(str(i)+": "+f["username"] for i,f in enumerate(followers))
        print(string)

    def get_following(self, prompt, args):
        following = []
        next_max_id = True
        while next_max_id:
            # first iteration hack
            if next_max_id is True:
                next_max_id = ''
            _ = prompt.api.getUserFollowings(prompt.id, maxid=next_max_id)
            following.extend(prompt.api.LastJson.get('users', []))
        next_max_id = prompt.api.LastJson.get('next_max_id', '')
        string = "\n\t"+"\n\t".join(str(i)+": "+f["username"] for i,f in enumerate(following))
        print(string)

    def exit_(self,prompt,args):
        return True