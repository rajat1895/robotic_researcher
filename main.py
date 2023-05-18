from robotics import Robot

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

robot = Robot("Quandrinaut")


def introduce_yourself():
    robot.say_hello()


def main():
    introduce_yourself()
    for scientist in SCIENTISTS:
        robot.open_wikipedia_page(scientist)
        robot.extract_scientist_information()
    robot.say_goodbye()
    robot.close_browser()


if __name__ == "__main__":
    main()
