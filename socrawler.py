#!/usr/bin/env python3.5

import requests
import sys


def get_questions(tag, N):
    '''
    Gets and sort N top questions based on a given tag in
    high low order by votes.
    Return:
        * link
        * title
        * score: votes
        * question_id: used to get answers identified by a sets of ids
        * author: display name
    '''
    url = 'https://api.stackexchange.com/'
    endpoint = ('questions?order=desc&sort=votes&pagesize={0}'
                '&tagged={1}&site=stackoverflow').format(N, tag)
    response = requests.get(url + endpoint)
    response = response.json()
    '''
      Filter data in JSON data above
    '''
    result = []
    for elem in response['items']:
        link = elem['link']
        title = elem['title']
        votes = elem['score']
        question_id = elem['question_id']
        author = elem['owner']['display_name']
        result.append((link, title, votes,
                       question_id, author))
    return result


def get_answers(question_id):
    '''
    Get the highest upvoted answer to the
    question identified in id.
    Return:
        * answer_id
        * score
    '''
    url = 'https://api.stackexchange.com/'
    endpoint = ('questions/' + str(question_id) + '/answers?'
                'sort=votes&pagesize=1&order=desc&'
                'site=stackoverflow')
    response = requests.get(url + endpoint)
    response = response.json()
    result = []
    for elem in response['items']:
        result.append((elem['answer_id'], elem['score']))
    return result


if __name__ == '__main__':
    tag = sys.argv[2]
    N = sys.argv[1]
    questions = get_questions(tag, N)
    for question in questions:
        url = question[0] + '#'  # URL of the question
        print('| ' + str(question[2]) + ' | ', question[1])
        print('|      | ', question[4])
        print('-' * 20)
        for tpl in get_answers(question[3]):
            url_answer = url + str(tpl[0])  # Create url of
            print('| ' + str(tpl[1]) + ' | ', url_answer)
        print('-' * 65 + '\n')
