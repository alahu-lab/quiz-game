import json
import os

# state.json은 main.py와 같은 폴더(프로젝트 루트)에 저장한다.
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


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

    def to_dict(self):
        """JSON으로 저장할 수 있는 딕셔너리로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리에서 Quiz를 만든다. 형식이 이상하면 ValueError를 낸다."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        if not isinstance(question, str) or question.strip() == "":
            raise ValueError("문제가 올바르지 않습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if (
            not isinstance(answer, int)
            or isinstance(answer, bool)
            or not 1 <= answer <= 4
        ):
            raise ValueError("정답 번호가 올바르지 않습니다.")
        return Quiz(question, [str(choice) for choice in choices], answer)


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


def read_text(prompt):
    """비어 있지 않은 문자열을 입력받는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("[!] 빈 입력입니다. 내용을 입력하세요.")
            continue
        return text


class QuizGame:
    """게임 전체(퀴즈 목록, 최고 점수, 메뉴 흐름, 파일 저장)를 관리한다."""

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0
        self.load_state()

    def reset_to_default(self):
        """기본 퀴즈와 빈 점수 기록으로 되돌린다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0

    def save_state(self):
        """퀴즈와 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"[!] 저장 중 오류가 발생했습니다: {error}")

    def load_state(self):
        """state.json에서 데이터를 불러온다. 없거나 망가졌으면 기본값을 쓴다."""
        if not os.path.exists(STATE_FILE):
            self.reset_to_default()
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data["best_score"]
            best_correct = data["best_correct"]
            best_total = data["best_total"]
            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")
            if not isinstance(best_correct, int) or not isinstance(best_total, int):
                raise ValueError("점수 기록 형식이 올바르지 않습니다.")
        except (OSError, KeyError, TypeError, ValueError):
            # json.JSONDecodeError, UnicodeDecodeError는 ValueError의 한 종류다.
            print("[!] 데이터 파일을 읽을 수 없어 기본 퀴즈로 초기화합니다.")
            self.reset_to_default()
            self.save_state()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total
        best_text = "없음" if best_score is None else f"{best_score}점"
        print(
            f"저장된 데이터를 불러왔습니다. "
            f"(퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})"
        )

    def show_menu(self):
        print("=" * 40)
        print("        나만의 게임 퀴즈")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play_quiz(self):
        if not self.quizzes:
            print("[!] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n퀴즈를 시작합니다! (총 {total}문제)")

        for index, quiz in enumerate(self.quizzes, start=1):
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
        self.update_best_score(correct, total)

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")
        question = read_text("문제를 입력하세요: ")
        choices = []
        for number in range(1, 5):
            choices.append(read_text(f"선택지 {number}: "))
        answer = read_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        if not self.quizzes:
            print("[!] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40)

    def update_best_score(self, correct, total):
        score = correct * 100 // total
        print(f"이번 점수: {score}점")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total
            self.save_state()
            print("새로운 최고 점수입니다!")

    def show_best_score(self):
        if self.best_score is None:
            print("[!] 아직 퀴즈를 풀지 않았습니다.")
            return
        print(
            f"\n최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
        )

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 5)
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    self.save_state()
                    print("게임을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 저장 후 안전하게 종료합니다.")
            self.save_state()


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()