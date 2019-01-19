import requests

from collections import OrderedDict

req_ses = requests.Session()


def get_eth_price():
    price_res = req_ses.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD&extraParams=cent&_=')
    return price_res.json()['USD']

def get_bounty_amount(bounty_url):
    bounty_res = req_ses.get(bounty_url)
    return bounty_res.json()['results']
        
def is_bounty_large_enough(amount):
    bounty_value = amount * get_eth_price()
    #if bounty_value >= 5:
    if bounty_value > 0.1:
        return bounty_value
    return False

def print_one_liners(list_to_print):
    for d in list_to_print:
        print('A new post titled:', d['title'], ', with bounty value $', d['bounty_value'], 'and ',
              d['bounty_recipients'], 'recipients has been posted. It has', d['answer_count'], 'answer(s) so far.')

if __name__ == '__main__':
    
    list_to_print = []
    
    ques_ids_string = ''
    
    post_res = req_ses.get('https://beta.cent.co/data/question?sort=new&range=1&_=')
    
    for post in post_res.json()['results']:
        question_id = post['id']
        has_no_bounty = post['closed']

        if has_no_bounty == 0:
            ques_ids_string += str(question_id) + '%2C' 

    ques_ids_string = ques_ids_string[:-3]
    bounty_url = 'https://beta.cent.co/data/bounty?questionIDs={}&_='.format(ques_ids_string)
    bounty_list = get_bounty_amount(bounty_url)
    for bounty in bounty_list:
        amount = bounty['amount']
        bounty_value = is_bounty_large_enough(amount)
        if bounty_value:
            for post in post_res.json()['results']:
                if post['id'] == bounty['question_id']:
                    dic = OrderedDict()
                    dic['title'] = post['title']
                    dic['body'] = post['body']
                    dic['answer_count'] = post['answer_count']
                    dic['bounty_recipients'] = post['recipients']
                    dic['bounty_value'] = bounty_value
                    list_to_print.append(dic)
    
    print_one_liners(list_to_print)
