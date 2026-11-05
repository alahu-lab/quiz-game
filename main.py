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