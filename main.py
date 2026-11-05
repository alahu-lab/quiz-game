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

def play_quiz(quizzes):
    """퀴즈를 모두 출제하고 (맞힌 개수, 전체 개수)를 돌려준다."""
    if not quizzes:
        print("[!] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
        return None

    total = len(quizzes)
    correct = 0
    print(f"\n퀴즈를 시작합니다! (총 {total}문제)")

    for index, quiz in enumerate(quizzes, start=1):
        print("-" * 40)
        print(f"[문제 {index}]")
        quiz.show()
        user_answer = read_number("정답 입력: ", 1, 4)
        if quiz.check_answer(user_answer):
            print("정답입니다!")
            correct += 1
        else:
            print(f"틀렸습니다. 정답은 {quiz.answer}번입니다.")

    score = correct * 100 // total
    print("=" * 40)
    print(f"결과: {total}문제 중 {correct}문제 정답! ({score}점)")
    print("=" * 40)
    return correct, total
def read_text(prompt):
    """비어 있지 않은 문자열을 입력받는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("[!] 빈 입력입니다. 내용을 입력하세요.")
            continue
        return text


def add_quiz(quizzes):
    """새 퀴즈를 입력받아 quizzes 리스트에 추가한다."""
    print("\n새로운 퀴즈를 추가합니다.")
    question = read_text("문제를 입력하세요: ")
    choices = []
    for number in range(1, 5):
        choices.append(read_text(f"선택지 {number}: "))
    answer = read_number("정답 번호 (1-4): ", 1, 4)
    quizzes.append(Quiz(question, choices, answer))
    print("퀴즈가 추가되었습니다!")
def show_quiz_list(quizzes):
    """등록된 퀴즈의 문제를 번호와 함께 보여준다."""
    if not quizzes:
        print("[!] 등록된 퀴즈가 없습니다.")
        return

    print(f"\n등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("-" * 40)
    for index, quiz in enumerate(quizzes, start=1):
        print(f"[{index}] {quiz.question}")
    print("-" * 40)
def main():
    quizzes = create_default_quizzes()
    try:
        while True:
            show_menu()
            choice = read_number("선택: ", 1, 5)
            if choice == 1:
                play_quiz(quizzes)
            elif choice == 2:
                add_quiz(quizzes)
            elif choice == 3:
                show_quiz_list(quizzes)
            elif choice == 5:
                print("게임을 종료합니다.")
                break
            else:
                print(f"(준비 중) {choice}번 기능입니다.")
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 안전하게 종료합니다.")

if __name__ == "__main__":
    main()