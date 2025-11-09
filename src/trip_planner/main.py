#!/usr/bin/env python
"""여행 플래너 CrewAI 메인 진입점"""

from textwrap import dedent
from trip_planner.crew import TripCrew


def run():
    """여행 플래너 Crew를 실행합니다"""
    print("## 여행 플래너 크루에 오신 것을 환영합니다")
    print('-------------------------------')

    location = input(
        dedent("""
          어디에서 출발하시나요?
        """))

    cities = input(
        dedent("""
          방문하고 싶은 도시 옵션은 무엇인가요?
        """))

    date_range = input(
        dedent("""
          여행하고 싶은 날짜 범위는 언제인가요?
        """))

    interests = input(
        dedent("""
          당신의 주요 관심사와 취미는 무엇인가요?
        """))

    inputs = {
        'origin': location,
        'cities': cities,
        'date_range': date_range,
        'interests': interests
    }

    trip_crew = TripCrew()
    result = trip_crew.crew().kickoff(inputs=inputs)

    print("\n\n########################")
    print("## 여행 계획입니다")
    print("########################\n")
    print(result)


def train():
    """
    Crew를 훈련합니다
    n_iterations: 훈련 반복 횟수
    """
    inputs = {
        'origin': "서울",
        'cities': "도쿄, 오사카, 교토",
        'date_range': "2024년 12월 1일 ~ 7일",
        'interests': "문화, 음식, 역사"
    }

    trip_crew = TripCrew()

    try:
        trip_crew.crew().train(
            n_iterations=int(input("훈련 반복 횟수를 입력하세요: ")),
            filename="trained_agents_data.pkl",
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"훈련 오류: {e}")


def replay():
    """
    이전 실행을 재생합니다
    """
    try:
        trip_crew = TripCrew()
        trip_crew.crew().replay(task_id=input("재생할 태스크 ID를 입력하세요: "))
    except Exception as e:
        raise Exception(f"재생 오류: {e}")


def test():
    """
    Crew를 테스트합니다
    """
    inputs = {
        'origin': "서울",
        'cities': "도쿄, 오사카, 교토",
        'date_range': "2024년 12월 1일 ~ 7일",
        'interests': "문화, 음식, 역사"
    }

    trip_crew = TripCrew()

    try:
        trip_crew.crew().test(
            n_iterations=int(input("테스트 반복 횟수를 입력하세요: ")),
            openai_model_name="gpt-4o-mini",
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"테스트 오류: {e}")
