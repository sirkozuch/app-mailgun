import codecs
import requests
import datetime
import pandas as pd
#from keboola import docker
from mailgun_fun.mailgun import send_complex_message


### Setting up the docker environment
cfg = docker.Config('/data/')
mailing_list_name = cfg.get_parameters()['mailing_list']
USER = cfg.get_parameters()['USER']
PASSWORD = cfg.get_parameters()['#token']
from_id = cfg.get_parameters()['from_id']
subject = cfg.get_parameters()['subject']
html_name = cfg.get_parameters()['html_body']
url = cfg.get_parameters()['url']

try:
    delivery_time = cfg.get_parameters()['delivery_time']
except NameError:
    delivery_time = '09:00:00 -0000'

scheduled_delivery_date = datetime.datetime.\
                            today().strftime('%a, %d %b %Y ') + delivery_time


path_html = '/data/in/files/' + html_name
html_file = codecs.open(path, 'r').read()


mailing_list_path = '/data/in/tables/' + mailing_list_name
mailing_list = pd.read_csv(filepath_or_buffer=mailing_list_path)


for index, row in mailing_list.iterrows():
    html_body = html_file % row
    to_id = '%(name)s <%(email)s>' % row

    send_status = send_complex_message(to_id,
                                       from_id, 
                                       subject,
                                       html_body,
                                       scheduled_delivery_date)

    if send_status.ok:
        print('Mail to %(email)s has been sent' % row)