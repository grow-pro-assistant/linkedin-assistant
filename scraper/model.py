class Profile:
    def __init__(self, name, bio, followers, following, posts):
        """
        Initialize the Profile class with profile data.

        Args:
            name (str): The name of the profile.
            bio (str): The bio of the profile.
            followers (int): The number of followers of the profile.
            following (int): The number of profiles the profile is following.
            posts (list): A list of Post objects representing the posts of the profile.
        """
        self.name = name
        self.bio = bio
        self.followers = followers
        self.following = following
        self.posts = posts

class Post:
    def __init__(self, title, text, shared_urls, connection_dist):
        """
        Initialize the Post class with post data.

        Args:
            title (str): The title of the post.
            text (str): The text of the post.
            shared_urls (list): A list of URLs shared in the post.
        """
        self.title = title
        self.text = text
        self.shared_urls = shared_urls
        self.connection_dist = connection_dist
        # self.page = page
