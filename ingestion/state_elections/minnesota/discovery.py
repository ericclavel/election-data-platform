import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin


RESULTS_URL = "https://electionresults.sos.mn.gov/170"

def fetch_html():
    request = urllib.request.Request(
        RESULTS_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/153.0.0.0 Safari/537.36"
            )
        },
    )

    with urllib.request.urlopen(request) as response:
        final_url = response.geturl()

        print("Final URL:", final_url)
        print("Status:", response.status)

        html = response.read().decode("utf-8")

        print("State General Election" in html)

        html = response.read().decode("utf-8")
    return html


def find_general_election_links(html):
    parser = ElectionLinkParser()
    parser.feed(html)



class ElectionLinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            print("Link tag found:", attrs)


    def handle_data(self, data):
        pass


    def handle_endtag(self, tag):
        pass





if __name__=="__main__":
    html = fetch_html()
    find_general_election_links(html)