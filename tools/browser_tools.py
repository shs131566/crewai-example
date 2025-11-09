import json
import os

import requests
from crewai import Agent, Task, Crew
from crewai.tools import tool
from unstructured.partition.html import partition_html


@tool("웹사이트 스크래핑 및 요약")
def scrape_and_summarize_website(website: str) -> str:
    """웹사이트 콘텐츠를 스크랩하고 요약하는 데 유용합니다"""
    url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in content:
        agent = Agent(
            role='수석 연구원',
            goal='작업 중인 콘텐츠를 기반으로 놀라운 연구 및 요약을 수행합니다',
            backstory="당신은 대기업의 수석 연구원이며 주어진 주제에 대한 연구를 수행해야 합니다.",
            allow_delegation=False)
        task = Task(
            agent=agent,
            description=f'아래 콘텐츠를 분석하고 요약하세요. 요약에 가장 관련성 높은 정보를 포함해야 하며, 요약만 반환하고 다른 것은 반환하지 마세요.\n\n콘텐츠\n----------\n{chunk}',
            expected_output='콘텐츠의 간결한 요약'
        )
        crew = Crew(agents=[agent], tasks=[task], verbose=False)
        summary = crew.kickoff()
        summaries.append(str(summary))
    return "\n\n".join(summaries)


class BrowserTools():
    scrape_and_summarize_website = scrape_and_summarize_website
