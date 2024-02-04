from dataclasses import dataclass
from enum import Enum
import sys

MAX_INVEST_LEVEL = 20
INF = 10**18

@dataclass
class Project:
    """プロジェクトクラス
    Note:
        プロジェクトの要素を持つ
    Attributes
        h (int): 残務量
        v (int): 価値
    """
    h: int
    v: int

@dataclass
class Project_Value:
    """プロジェクトの価値を管理するクラス
    Note:
        プロジェクトの要素を持つ
    Attributes
        idx (int): プロジェクトのインデックス
        value (float): プロジェクトの評価値(価値/残務量)
        workload (int): プロジェクトの残務量
    """
    idx: int
    value: float
    workload: int

class CardType(Enum):
    """方針カードクラス
    Note:
        方針カードの種類を列挙
    Attributes
    """
    WORK_SINGLE = 0
    WORK_ALL = 1
    CANCEL_SINGLE = 2
    CANCEL_ALL = 3
    INVEST = 4

@dataclass
class Card:
    """カードクラス
    Note:
        各方針カードの個体値を管理
    Attributes
        t (int): 方針カードの種類
        w (int): 労働力
        p (int): 補充する方針カードのコスト
    """
    t: CardType
    w: int
    p: int

class Judge:
    """ジャッジクラス
    Note:
        ジャッジとのやり取りを管理
    Attributes
        n (int): 手札の枚数
        m (int): 管理するプロジェクトの個数
        k (int): 補充する方針カードの候補数
    """

    def __init__(self, n: int, m: int, k: int):
        self.n = n
        self.m = m
        self.k = k

    def read_initial_cards(self) -> list[Card]:
        """最初の手札をロードする
        """
        cards = []
        for _ in range(self.n):
            t, w = map(int, input().split())
            cards.append(Card(CardType(t), w, 0))
        return cards

    def read_projects(self) -> list[Project]:
        """最初orカード使用後のプロジェクトの状況の情報を標準入力から受け取る
        """
        projects = []
        for _ in range(self.m):
            h, v = map(int, input().split())
            projects.append(Project(h, v))
        return projects

    def use_card(self, c: int, m: int) -> None:
        """方針カードを使う

        Args:
            c (int): 使う方針カードの番号
            m (int): カードの効果を適用するプロジェクトの番号(全力労働カード、業務転換カード、増資カードの場合はm=0)
        """
        print(f"{c} {m}", flush=True)

    def read_money(self) -> int:
        """現在の所持金の情報を標準入力から受け取る
        """
        return int(input())

    def read_next_cards(self) -> list[Card]:
        """手札に補充する方針カードの候補の情報を標準入力から受け取る
        """
        cards = []
        for _ in range(self.k):
            t, w, p = map(int, input().split())
            cards.append(Card(CardType(t), w, p))
        return cards

    def select_card(self, r: int) -> None:
        """K枚の方針カード候補のうち何番目のカードを手札に加えるかの情報を標準出力へ出力する

        Args:
            r (int): 補充する方針カードの番号
        """
        print(r, flush=True)

    def comment(self, message: str) -> None:
        print(f"# {message}")


class Solver:
    """ソルバクラス
    Note:
        解法を記載するクラス
    Attributes
        n (int): 手札の枚数
        m (int): 管理するプロジェクトの個数
        k (int): 補充する方針カードの候補数
        t (int): ターン数(常に1000)
    """
    def __init__(self, n: int, m: int, k: int, t: int):
        self.n = n
        self.m = m
        self.k = k
        self.t = t
        self.judge = Judge(n, m, k)

    def solve(self) -> int:
        self.turn = 0
        self.money = 0
        self.invest_level = 0
        self.cards = self.judge.read_initial_cards()
        self.projects = self.judge.read_projects()
        self.owned_card_num = {CardType.WORK_SINGLE:0, CardType.WORK_ALL:0, CardType.CANCEL_SINGLE:0, CardType.CANCEL_ALL:0, CardType.INVEST:0}
        self.prior_projects = []
        self.total_projects_value = 0
        self.total_work_resource = 0
        self.total_workload = 0
        self.cancel_criteria = 0
        self.total_workload = 0

        # T(=1000)ターン分の行動を記載
        for _ in range(self.t):
            use_card_i, use_target = self._select_action()
            if self.cards[use_card_i].t == CardType.INVEST:
                self.invest_level += 1
            # example for comments
            self.judge.comment(f"used {self.cards[use_card_i]} to target {use_target}")
            self.judge.use_card(use_card_i, use_target)
            assert self.invest_level <= MAX_INVEST_LEVEL

            self.projects = self.judge.read_projects()
            self.money = self.judge.read_money()

            next_cards = self.judge.read_next_cards()
            select_card_i = self._select_next_card(next_cards)
            self.cards[use_card_i] = next_cards[select_card_i]
            self.judge.select_card(select_card_i)
            self.money -= next_cards[select_card_i].p
            assert self.money >= 0

            self.turn += 1

        return self.money

    def _select_action(self) -> tuple[int, int]:
        """使用する方針カードを決定する
        """
        # TODO: 増資カードはとにかく使ったほうが良さそう？？
        # TODO: 労働カードは残務量が少ないプロジェクトに優先的に使いたい
        # TODO: キャンセルカードは、価値/残務量が一定以下の場合に使いたい(残務量が2**5 * 2**invest_levelを超え、価値が5*2**invest_levelより低いとやばい)
        # TODO: 業務転換カードは、トータルの価値/残務量が一定以下の場合に使いたい
        # TODO: 全力労働カードは、管理しているプロジェクトのトータル残務量が多い時に使いたい(業務転換カードとのコンボはどうか？)

        # トータルのプロジェクトの価値を計算
        self._evaluate_projects()

        # 今持ってるカードの使用優先度を決める(4>3>2>1>0)
        work_single = []
        work_all = []
        cancel_single = []
        cancel_all = []
        invest = []
        for idx, card in enumerate(self.cards):
            match card.t:
                case CardType.WORK_SINGLE:
                    work_single.append((idx, card.w))
                case CardType.WORK_ALL:
                    work_all.append((idx, card.w))
                case CardType.CANCEL_SINGLE:
                    cancel_single.append(idx)
                case CardType.CANCEL_ALL:
                    cancel_all.append(idx)
                case CardType.INVEST:
                    invest.append(idx)

        work_single.sort(key=lambda x:-x[1])
        work_all.sort(key=lambda x:-x[1])

        m = 0
        self.cancel_criteria = (15 * (2**self.invest_level)) / (32 * 2**self.invest_level)
        self.work_all_criteria = 15 * (2**self.invest_level) * self.m
        if len(invest) > 0 and self.invest_level < MAX_INVEST_LEVEL:
            card_idx = invest[0]
            assert 0 <= card_idx < self.n
            assert 0 <= m < self.m
            return (card_idx, m)
        elif len(cancel_all) > 0 and self.total_workload > (self.total_work_resource+1)*50:
            card_idx = cancel_all[0]
            assert 0 <= card_idx < self.n
            assert 0 <= m < self.m
            return (card_idx, m)
        elif len(cancel_single) > 0 and self.prior_projects[-1].value < self.cancel_criteria:
            card_idx = cancel_single[0]
            m = self.prior_projects[-1].idx
            assert 0 <= card_idx < self.n
            assert 0 <= m < self.m
            return (card_idx, m)
        elif len(work_all) > 0 and self.total_workload > self.work_all_criteria:
            card_idx = work_all[0][0]
            assert 0 <= card_idx < self.n
            assert 0 <= m < self.m
            return (card_idx, m)
        elif len(work_single) > 0:
            ma_value = 0
            ma_card_idx, ma_project_idx = -1,-1
            for card_idx,w in work_single:
                for project_idx,project in enumerate(self.projects):
                    if w >= project.h and project.v > ma_value:
                        ma_value = project.v
                        ma_card_idx = card_idx
                        ma_project_idx = project_idx
            if ma_card_idx != -1 and ma_project_idx != -1:
                assert 0 <= ma_card_idx < self.n
                assert 0 <= ma_project_idx < self.m
                return (ma_card_idx, ma_project_idx)
            card_idx = work_single[0][0]
            m = self.prior_projects[0].idx
            assert 0 <= card_idx < self.n
            assert 0 <= m < self.m
            return (card_idx, m)            
        else:
            if self.cards[0].t in [CardType.WORK_SINGLE, CardType.CANCEL_SINGLE]:
                m = self.prior_projects[0].idx
            return (0,m)


    def _evaluate_projects(self):
        """各プロジェクト及び全プロジェクト通しての価値を評価

        Note:
            self.projectsを元に、優先度順にソートしたプロジェクト(self.prior_projects)と
            全プロジェクトトータルの評価値を求める
        """
        self.prior_projects = []
        self.total_projects_value = 0
        self.total_workload = 0
        for idx, project in enumerate(self.projects):
            project_value = project.v / (project.h**1.1 * (self.turn+1)**1.1)
            self.total_projects_value += project_value
            self.total_workload += project.h
            self.prior_projects.append(Project_Value(idx, project_value, project.h))
        self.prior_projects.sort(key=lambda x:-x.value)


    def _select_next_card(self, next_cards: list[Card]) -> int:
        """補充する方針カードを決定する

        Note:
            t = 0の場合、1<=p<=10000 * 2**invest_level ※pは正規分布に従う
            t = 1の場合、1<=p<=10000 * 2**invest_level ※pは正規分布に従う
            t = 2の場合、0<=p<=10 * 2**invest_level ※pは一様分布に従う
            t = 3の場合、0<=p<=10 * 2**invest_level ※pは一様分布に従う
            t = 4の場合、200<=p<=1000 * 2**invest_level ※pは一様分布に従う

        Attributes
            next_cards (list[Card]): 補充する方針カードの候補
        """
        # TODO: 基本的にお買い得なカードを買っていきたい(t=0ならwに対してp<w/(2**invest_level)か、t=1ならwに対してp<w/(2**invest_level)*Mか)
        # TODO: t=2,3ならp<5 * 2**invest_levelか(ただし、プロジェクトの状況による。ブラックプロジェクトばかりなら優先的にやめたい)
        # TODO: お金が無いなら0番目のカード
        self.average_work_resource = 0
        self.owned_card_num = {CardType.WORK_SINGLE:0, CardType.WORK_ALL:0, CardType.CANCEL_SINGLE:0, CardType.CANCEL_ALL:0, CardType.INVEST:0}
        for card in self.cards:
            self.owned_card_num[card.t] += 1
            if card.t in [CardType.WORK_SINGLE, CardType.WORK_ALL]:
                self.average_work_resource += card.w
        if (self.owned_card_num[CardType.WORK_SINGLE] + self.owned_card_num[CardType.WORK_ALL]) != 0:
            self.average_work_resource /= (self.owned_card_num[CardType.WORK_SINGLE] + self.owned_card_num[CardType.WORK_ALL])
        card_value = [[idx,self.k-idx] for idx in range(self.k)]
        for idx, card in enumerate(next_cards):
            if self.money < card.p:
                card_value[idx][1] = -1
                continue
            card_value[idx][1] += self._calc_card_value(card)
        card_value.sort(key=lambda x:-x[1])
        card_idx, value = card_value[0]
        return card_idx
    
    def _calc_card_value(self, next_card: Card) -> int:
        """補充候補の方針カードの価値を計算する

        Note:

        Attributes
            next_card (Card): 補充する方針カードの候補
        Return
            card_value (int): 補充候補の方針カードの価値
        """
        # TODO: ターン数が経過するにつれ所持金の最大化を意識する
        # TODO: Mが小さい時はちょっとでもブラックプロジェクトなら爆破する
        # TODO: プロジェクト数が多いほどWORK_ALLの欲しさは増える
        card_price = 0
        match next_card.t:
            case CardType.WORK_SINGLE:
                if self.turn < 250:
                    if next_card.p < self.money / 2:
                        card_price = next_card.w**1.2 / ((next_card.p+1)) * max(0, self.m//2-self.owned_card_num[next_card.t])
                    else:
                        card_price = next_card.w / ((next_card.p+1)) * max(0, self.m//2-self.owned_card_num[next_card.t])
                else:
                    card_price = next_card.w / ((next_card.p+1)**2) * max(0, self.m//2-self.owned_card_num[next_card.t])
            case CardType.WORK_ALL:
                if next_card.p < next_card.w * self.m * 0.75:
                    card_price = (next_card.w**2) / ((next_card.p+1)**2) * max(0, self._clamp(self.m,5,6)-self.owned_card_num[next_card.t])
                else:
                    card_price = (next_card.w * self.m) / ((next_card.p+1)**2) * max(0, self._clamp(self.m,2,3)-self.owned_card_num[next_card.t])

            case CardType.CANCEL_SINGLE:
                if self.total_projects_value < self.cancel_criteria * self.m:
                    card_price = 1 / ((next_card.p+1)) * max(0, self._clamp(self.m,3,5)-self.owned_card_num[next_card.t])
                else:
                    card_price = 1 / ((next_card.p+1)**2) * max(0, self._clamp(self.m,3,5)-self.owned_card_num[next_card.t])
            case CardType.CANCEL_ALL:
                if self.total_projects_value < self.cancel_criteria * self.m and self.total_workload > (self.total_work_resource+1)*50:
                    card_price = 1 / ((next_card.p+1)) * max(0, 1-self.owned_card_num[next_card.t])
                else:
                    card_price = 1 / ((next_card.p+1)**2) * max(0, 1-self.owned_card_num[next_card.t])
            case CardType.INVEST:
                if self.turn < 800 and self.money > next_card.p * 1.1:
                    card_price = INF * max(0, self.n-self.owned_card_num[next_card.t])
                else:
                    card_price = -1

        return card_price

    def _clamp(self, n, smallest, largest):
        return max(smallest, min(n, largest))

def main():
    n, m, k, t = map(int, input().split())
    solver = Solver(n, m, k, t)
    score = solver.solve()

if __name__ == "__main__":
    main()
