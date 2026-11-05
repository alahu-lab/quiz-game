class Quiz:
    """퀴즈 한 문제를 표현한다."""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (문자열)
        self.choices = choices    # 선택지 4개가 담긴 리스트
        self.answer = answer      # 정답 번호 (1~4)

    def show(self):
        print(self.question)
        print()
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer
def create_default_quizzes():
    """기본 퀴즈 5개를 만들어 리스트로 돌려준다."""
    return [
        Quiz(
            "마인크래프트에서 엔더 드래곤이 있는 차원은?",
            ["오버월드", "네더", "디 엔드", "하늘 섬"],
            3,
        ),
        Quiz(
            "포켓몬스터에서 피카츄의 타입은?",
            ["노말", "전기", "불꽃", "물"],
            2,
        ),
        Quiz(
            "슈퍼 마리오의 마리오는 원래 어떤 직업일까?",
            ["요리사", "목수", "소방관", "배관공"],
            4,
        ),
        Quiz(
            "리그 오브 레전드 소환사의 협곡에서 한 팀의 인원은?",
            ["3명", "4명", "5명", "6명"],
            3,
        ),
        Quiz(
            "젤다의 전설 시리즈에서 플레이어가 조종하는 주인공의 이름은?",
            ["링크", "젤다", "가논", "미파"],
            1,
        ),
    ]
def show_menu():
    print("=" * 40)
    print("        나만의 게임 퀴즈")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def read_number(prompt, min_value, max_value):
    """min_value~max_value 사이의 숫자를 입력받는다. 잘못 입력하면 다시 묻는다."""
    guide = f"{min_value}-{max_value} 사이의 숫자를 입력하세요."
    while True:
        text = input(prompt).strip()
        if text == "":
            print(f"[!] 빈 입력입니다. {guide}")
            continue
        try:
            number = int(text)
        except ValueError:
            print(f"[!] 잘못된 입력입니다. {guide}")
            continue
        if number < min_value or number > max_value:
            print(f"[!] 범위를 벗어났습니다. {guide}")
            continue
        return number


def main():
    try:
        while True:
            show_menu()
            choice = read_number("선택: ", 1, 5)
            if choice == 5:
                print("게임을 종료합니다.")
                break
            print(f"(준비 중) {choice}번 기능입니다.")
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 안전하게 종료합니다.")


if __name__ == "__main__":
    main()