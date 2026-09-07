from dateutil import parser

class Article:
    def __init__(self, _id="", url="", date="", headline="", body=""):
        self.uuid = _id
        self.url = url
        self.date= parser.parse(date)
        self.headline = headline
        self.body = body.strip()
        self.headline = headline.strip()
    def __str__(self):
        return f"""
headline : {self.headline},
{self.date}
{self.body}

n°= {"Empty" if self.uuid == "" else self.uuid}
source : \"{self.url}\"
"""