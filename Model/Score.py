import time
from typing import Optional


class Score:
    PRE_DEFINED_TIME: float = 60

    def __init__(self):
        self.__points = 0
        self.__consecutive_correct = 0
        self.__start_time: Optional[float] = None

    def get_points(self) -> int:
        return self.__points

    def start_timer(self):
        self.__start_time = time.time()

    def __stop_timer_add_bonus(self):
        if not self.__start_time:
            return
        interval_time = time.time() - self.__start_time
        saved_time = Score.PRE_DEFINED_TIME - interval_time
        if saved_time > 0:
            bonus = int(saved_time / 30)
            self.__points += bonus

    def deduct(self):
        self.__points -= 1
        self.__consecutive_correct = 0

    def add_corrected_points(self):
        self.__points += 3
        if self.__consecutive_correct != 0:
            self.__points += self.__consecutive_correct + 1

        self.__consecutive_correct += 1
        self.__stop_timer_add_bonus()
        self.start_timer()

    def get_remaining_time(self) -> int:
        if self.__start_time is None:
            return int(Score.PRE_DEFINED_TIME)
        elapsed_time = time.time() - self.__start_time
        remaining_time = int(Score.PRE_DEFINED_TIME - elapsed_time)
        return max(remaining_time, 0)

    def get_scoring_info(self) -> str:
        return """
        <html>
            <body>
                <ul>
                    <li><b>Correct match:</b> 3 points.</li>
                    <li><b>Additional consecutive matches:</b> +1 point for each consecutive correct match.</li>
                    <li><b>Incorrect match:</b> -1 point.</li>
                    <li><b>Time bonus:</b> Extra points based on time saved (1 point for every 30 seconds saved).</li>
                    <li><b>Hint used:</b> -1 point if a set is available.</li>
                    <li><b>Draw cards although a set is available:</b> -1 point.</li>
                </ul>
            </body>
        </html>
        """