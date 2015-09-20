from xml.dom import minidom
import requests


def lookup_cc(cc_number):
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
