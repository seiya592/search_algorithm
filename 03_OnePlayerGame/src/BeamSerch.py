import copy
import heapq
import time
import random
import const

from Greedy import GreedyMazeState
from WithTime import TimeKeeper

class BeamSearchMazeState(GreedyMazeState):
    first_action: int

    def __init__(self, seed):
        super().__init__(seed)
        self.first_action = -1

    def __lt__(self, other):
        other: BeamSearchMazeState
        return -self.evaluated_score < -other.evaluated_score

    # def __gt__(self, other):
    #     other: BeamSearchMazeState
    #     return -self.evaluated_score > -other.evaluated_score


def beam_search_action_with_time_threshold(state: BeamSearchMazeState, beam_width: int, beam_depth: int, time_threshold: int):
    now_beam: list[BeamSearchMazeState]
    best_state: BeamSearchMazeState
    next_beam: list[BeamSearchMazeState]

    now_beam = []
    heapq.heapify(now_beam)

    heapq.heappush(now_beam, state)

    time_keeper = TimeKeeper(time_threshold)
    best_state = 0

    for t in range(beam_depth):
        next_beam = []
        heapq.heapify(next_beam)
        for _ in range(beam_width):
            if not len(now_beam):
                break
            if time_keeper.is_time_over():
                if best_state:
                    return best_state.first_action
            now_state = heapq.heappop(now_beam)
            for action in now_state.legal_actions():
                next_state = copy.deepcopy(now_state)
                next_state.advance(action)
                next_state.evaluate_score()
                if not t:
                    next_state.first_action = action
                heapq.heappush(next_beam, next_state)

        now_beam = next_beam
        best_state = next_beam[0]

        if best_state.is_done():
            break
    return best_state.first_action


def beam_search_action(state: BeamSearchMazeState, beam_width: int, beam_depth: int):
    now_beam: list[BeamSearchMazeState]
    best_state: BeamSearchMazeState
    next_beam: list[BeamSearchMazeState]

    now_beam = []
    heapq.heapify(now_beam)

    heapq.heappush(now_beam, state)

    for t in range(beam_depth):
        next_beam = []
        heapq.heapify(next_beam)
        for _ in range(beam_width):
            if not len(now_beam):
                break
            now_state = heapq.heappop(now_beam)
            for action in now_state.legal_actions():
                next_state = copy.deepcopy(now_state)
                next_state.advance(action)
                next_state.evaluate_score()
                if not t:
                    next_state.first_action = action
                heapq.heappush(next_beam, next_state)

        now_beam = next_beam
        best_state = next_beam[0]

        if best_state.is_done():
            break
    return best_state.first_action


def play_game(seed: int = const.RANDOM_SEED):
    state = BeamSearchMazeState(seed)
    # print(state)

    while not state.is_done():
        state.advance(beam_search_action(state, 2, const.END_TURN))
        # print(state)
    print(f'{state.__class__} {state.game_score}')


def play_game_time(seed: int = const.RANDOM_SEED):
    state = BeamSearchMazeState(seed)
    # print(state)

    while not state.is_done():
        state.advance(beam_search_action_with_time_threshold(state, 5, const.END_TURN, 10))
        # print(state)
    print(f'{state.__class__} {state.game_score}')


def test_ai_score(game_number: int):
    # 乱数生成器のシードを設定
    seed = time.time()
    random.seed(seed)

    score_mean = 0  # game_number回分の合計スコア

    for i in range(game_number):
        state = BeamSearchMazeState(random.randrange(const.INF))

        while not state.is_done():
            state.advance(beam_search_action(state, 2, const.END_TURN))
        score_mean += state.game_score

    print(f'Score : {score_mean / game_number}')


def test_ai_score_time(game_number: int):
    # 乱数生成器のシードを設定
    seed = time.time()
    random.seed(seed)

    score_mean = 0  # game_number回分の合計スコア

    for i in range(game_number):
        state = BeamSearchMazeState(random.randrange(const.INF))

        while not state.is_done():
            state.advance(beam_search_action_with_time_threshold(state, 5, const.END_TURN, 1))
        score_mean += state.game_score

    print(f'Score : {score_mean / game_number}')