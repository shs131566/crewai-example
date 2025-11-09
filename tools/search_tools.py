import json
import os

import requests
from crewai.tools import tool


@tool("인터넷 검색")
def search_internet(query: str) -> str:
    """주어진 주제에 대해 인터넷을 검색하고 관련 결과를 반환하는 데 유용합니다"""
    top_result_to_return = 4
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # check if there is an organic key
    if 'organic' not in response.json():
        return "죄송합니다. 해당 내용을 찾을 수 없습니다. serper API 키에 오류가 있을 수 있습니다."
    else:
        results = response.json()['organic']
        string = []
        for result in results[:top_result_to_return]:
            try:
                string.append('\n'.join([
                    f"제목: {result['title']}", f"링크: {result['link']}",
                    f"요약: {result['snippet']}", "\n-----------------"
                ]))
            except KeyError:
                next

        return '\n'.join(string)


class SearchTools():
    search_internet = search_internet
