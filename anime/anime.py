class Anime:
    def __init__(self, anime_name=None, link=None, ep=None):
        self.anime_name = anime_name
        self.link = link
        self.ep = ep

    def get_link(self, base_url):
        pass

    def download(self):
        pass
