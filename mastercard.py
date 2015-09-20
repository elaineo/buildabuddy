from xml.dom import minidom
import requests


def lookup_cc(cc_number):
    """
    lookup_cc('5343434343434343') # stolen
    lookup_cc('5105105105105100') # fraud
    lookup_cc('6011111111111117') # unauthorized use
    lookup_cc('5305305305305300') # capture card
    lookup_cc('5222222222222200') # lost
    lookup_cc('4444333322221111') # counterfeit
    lookup_cc('343434343434343') # no listed
    """
    d = {}
    headers = {'Content-Type': 'application/xml'}
    xml_body = '<AccountInquiry><AccountNumber>%s</AccountNumber></AccountInquiry>' % cc_number
    url = 'http://dmartin.org:8019/fraud/loststolen/v1/account-inquiry?Format=XML'
    r = requests.put(url, data=xml_body, headers=headers)

    try:
        xml = minidom.parseString(r.content)
        elem = xml.getElementsByTagName('Listed')[0]
        listed = elem.childNodes[0].nodeValue
        d['listed'] = listed
        elem = xml.getElementsByTagName('Status')[0]
        status = elem.childNodes[0].nodeValue
        d['status'] = status
        elem = xml.getElementsByTagName('ReasonCode')[0]
        reason_code = elem.childNodes[0].nodeValue
        d['reason_code'] = reason_code
        elem = xml.getElementsByTagName('Reason')[0]
        reason = elem.childNodes[0].nodeValue
        d['reason'] = reason
    except:
        pass
    return d
