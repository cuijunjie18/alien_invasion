from pathlib import Path
import json
class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self,ai_game):
        """初始化统计信息"""
        self.read_high_score()
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """初始化游戏运行期间可能发生变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def read_high_score(self):
        """从文件中读取json类文件最高分"""
        self.path = Path('high_score_record.json')
        self.high_score = json.loads(self.path.read_text())

