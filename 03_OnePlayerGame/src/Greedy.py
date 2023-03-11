import copy

from MazeState import MazeState
import const
import time
import random


class GreedyMazeState(MazeState):

    def __init__(self, seed):
        super().__init__(seed)
        self.evaluated_score = 0

    def evaluate_score(self) -> None:
        """
        探索用の盤面評価をする
        :return: None
        """
        self.evaluated_score = self.game_score


def greedy_action(state: GreedyMazeState) -> int:
    legal_action = state.legal_actions()
    best_score = -const.INF
    best_action = -1
    for action in legal_action:             # 実行可能なアクションでループ
        now_state = copy.deepcopy(state)
        now_state.advance(action)
        now_state.evaluate_score()
        if now_state.evaluated_score > best_score:
            best_score = now_state.evaluated_score
            best_action = action
    return best_action


def play_game(seed: int = const.RANDOM_SEED):
    state = GreedyMazeState(seed)
    # print(state)

    while not state.is_done():
        state.advance(greedy_action(state))
        # print(state)
    print(f'{state.__class__} {state.game_score}')

def test_ai_score(game_number: int):
    # 乱数生成器のシードを設定
    seed = time.time()
    random.seed(seed)

    score_mean = 0  # game_number回分の合計スコア

    for i in range(game_number):
        state = GreedyMazeState(random.randrange(const.INF))

        while not state.is_done():
            state.advance(greedy_action(state))
        score_mean += state.game_score

    print(f'Score : {score_mean / game_number}')