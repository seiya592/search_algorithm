import time


class TimeKeeper():
    """
    時間経過管理
    """
    __start_time: int   # インスタンス生成時の時間
    __threshold: int    # ms単位で監視する時間を指定

    def __init__(self, threshold):
        self.__start_time = time.perf_counter_ns()
        self.__threshold = threshold

    def is_time_over(self) -> bool:
        """
        時間経過したかを確認
        :return:
        """
        return self.__threshold <= (time.perf_counter_ns() - self.__start_time) / 10**6