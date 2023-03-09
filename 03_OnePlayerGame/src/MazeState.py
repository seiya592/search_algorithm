import const
import random
import time


class Coord:
    """
    座標を保持するクラス
    """
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y


class MazeState:
    """
    数字集め迷路クラス
    """
    _points: list[list[int]]
    _turn: int
    character: Coord
    game_score: int

    def __init__(self, seed):
        # 乱数生成器のシードを設定
        random.seed(seed)
        # キャラクターの位置
        self.character = Coord(x=random.randrange(const.W), y=random.randrange(const.H))
        # 現在のターン数
        self._turn = 0
        # 現在のゲームスコア
        self.game_score = 0
        # 盤面生成(キャラクターの初期位置は0固定)
        self._points = [[random.randrange(0, 10) if not (x == self.character.x and y == self.character.y) else 0
                          for x in range(const.W)] for y in range(const.H)]

    def is_done(self) -> bool:
        """
        ゲームの終了判定
        :return: bool
        """
        return self._turn >= const.END_TURN

    def advance(self, action: int) -> None:
        """
        指定したアクションでゲームを1ターン進める
        :param action:
        :return:
        """
        self.character.x += const.DX[action]
        self.character.y += const.DY[action]
        self.game_score += self._points[self.character.y][self.character.x]
        self._points[self.character.y][self.character.x] = 0
        self._turn += 1

    def legal_actions(self) -> list:
        """
        現在の状況でプレイヤーが可能な行動を全て取得
        :return: list
        """
        actions = []
        for i in range(0,4):
            tx = self.character.x + const.DX[i]
            ty = self.character.y + const.DY[i]
            if 0 <= tx < const.W and 0 <= ty < const.H:
                actions.append(i)
        return actions

    def __str__(self) -> str:
        """
        現在のゲーム状況を文字列にする
        :return: str
        """
        ret = ''
        ret += f'turn: {self._turn}\n'
        ret += f'score: {self.game_score}\n'
        for h in range(const.H):
            for w in range(const.W):
                if h == self.character.y and w == self.character.x:
                    ret += '@'
                elif self._points[h][w]:
                    ret += f'{self._points[h][w]}'
                else:
                    ret += '.'
            ret += '\n'
        return ret


def random_action(state: MazeState):
    legal_action = state.legal_actions()
    return legal_action[random.randrange(len(legal_action))]


def play_game(seed: int = const.RANDOM_SEED):
    state = MazeState(seed)
    print(state)

    while not state.is_done():
        state.advance(random_action(state))
        print(state)


def test_ai_score(game_number: int):
    # 乱数生成器のシードを設定
    seed = time.time()
    random.seed(seed)

    score_mean = 0  # game_number回分の合計スコア

    for i in range(game_number):
        state = MazeState(random.randrange(const.INF))

        while not state.is_done():
            state.advance(random_action(state))
        score_mean += state.game_score

    print(f'Score : {score_mean / game_number}')
