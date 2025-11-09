from crewai import Task
from textwrap import dedent
from datetime import date

class TripTasks:

    def identify_task(self, agent, origin, cities, interests, range):
        return Task(
            description=dedent(f"""
                날씨 패턴, 계절별 이벤트, 여행 비용 등 특정 기준을
                바탕으로 여행에 가장 적합한 도시를 분석하고 선택하세요.
                이 작업은 현재 날씨 상황, 다가오는 문화 또는 계절 행사,
                전체적인 여행 경비 등의 요소를 고려하여 여러 도시를
                비교하는 것을 포함합니다.

                최종 답변은 선택한 도시에 대한 상세한 보고서여야 하며,
                실제 항공료, 날씨 예보, 명소를 포함하여 발견한 모든 것을
                담아야 합니다.
                {self.__tip_section()}

                출발지: {origin}
                도시 옵션: {cities}
                여행 날짜: {range}
                여행자 관심사: {interests}
            """),
            agent=agent,
            expected_output="항공료, 날씨 예보, 명소를 포함한 선택된 도시에 대한 상세한 보고서"
        )

    def gather_task(self, agent, origin, interests, range):
        return Task(
            description=dedent(f"""
                이 도시의 현지 전문가로서, 그곳을 여행하며 최고의 여행을
                원하는 사람을 위한 심층 가이드를 작성해야 합니다!
                주요 명소, 현지 관습, 특별 행사, 일일 활동 추천에 대한
                정보를 수집하세요.
                현지인만이 알 수 있는 종류의 장소인 최고의 명소를
                찾으세요.
                이 가이드는 숨겨진 보석 같은 곳, 문화적 핫스팟,
                필수 방문 랜드마크, 날씨 예보, 대략적인 비용을 포함하여
                도시가 제공하는 것에 대한 철저한 개요를 제공해야 합니다.

                최종 답변은 여행 경험을 향상시키기 위해 맞춤화된
                문화적 통찰력과 실용적인 팁이 풍부한 포괄적인 도시 가이드여야 합니다.
                {self.__tip_section()}

                여행 날짜: {range}
                출발지: {origin}
                여행자 관심사: {interests}
            """),
            agent=agent,
            expected_output="숨겨진 보석 같은 곳, 문화적 핫스팟, 실용적인 여행 팁을 포함한 포괄적인 도시 가이드"
        )

    def plan_task(self, agent, origin, interests, range):
        return Task(
            description=dedent(f"""
                이 가이드를 날씨 예보, 식사 장소, 짐 싸기 제안,
                예산 분석을 포함한 상세한 일일 계획이 있는 완전한
                7일 여행 일정으로 확장하세요.

                방문할 실제 장소, 머물 실제 호텔, 갈 실제 레스토랑을
                반드시 제안해야 합니다.

                이 일정은 도착부터 출발까지 여행의 모든 측면을 다루어야 하며,
                도시 가이드 정보를 실용적인 여행 물류와 통합해야 합니다.

                최종 답변은 일일 일정, 예상 날씨 상황, 권장 의류 및
                짐 싸기 항목, 상세한 예산을 포함하는 마크다운 형식의
                완전히 확장된 여행 계획이어야 하며, 최고의 여행을
                보장해야 합니다. 구체적으로 작성하고 각 장소를 선택한
                이유와 특별한 점을 설명하세요! {self.__tip_section()}

                여행 날짜: {range}
                출발지: {origin}
                여행자 관심사: {interests}
            """),
            agent=agent,
            expected_output="일일 일정, 날씨 상황, 짐 싸기 제안, 예산 분석을 포함한 완전한 확장 여행 계획"
        )

    def __tip_section(self):
        return "최선을 다하면 100달러 팁을 드립니다!"
