import MazeState
import Greedy
import BeamSerch

def main():
    MazeState.play_game()
    Greedy.play_game()
    BeamSerch.play_game_time()

    # MazeState.test_ai_score(100)
    # Greedy.test_ai_score(10)
    # BeamSerch.test_ai_score(100)
    # BeamSerch.test_ai_score_time(10)

if __name__ == '__main__':
    main()
