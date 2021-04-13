import requests
import lxml

from gi.repository import Notify
Notify.init("weatheralert")

def main(args):
    # Your state or region here:
    req = requests.get('https://alerts.weather.gov/cap/or.php?x=0')
    xml = req.content
    from lxml import etree
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    atom = etree.fromstring(xml)
    for element in atom.xpath('//atom:entry', namespaces=ns):
        title = ''
        text = ''
        for node in element.iterchildren():
            if node.tag.find("event") >-1:
                title = node.text
            elif node.tag.find("summary") >-1:
                text = node.text
        if text.find("There are no active watches, warnings or advisories") == -1:
            notification = Notify.Notification.new(title, text)
            notification.show()
        else:
            print("No alerts")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
