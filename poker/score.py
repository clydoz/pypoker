class Score:
    HIGHEST_CARD = 0
    PAIR = 1
    DOUBLE_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FULL_HOUSE = 5
    FLUSH = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    CATEGORIES = {
        0: "Highest Card",
        1: "Pair",
        2: "Double Pair",
        3: "Three of a Kind",
        4: "Straight",
        5: "Full House",
        6: "Flush",
        7: "Four of a Kind",
        8: "Straight Flush"}

    def __init__(self, category, cards):
        self._category = category
        self._cards = cards

    @property
    def category(self):
        """Gets the category for this score."""
        return self._category

    @property
    def cards(self, limit=0):
        return self._cards

    def cmp(self, other):
        """Compare scores. Returns:
        a positive integer if self is stronger than other,
        0 if the two scores are identical,
        a negative integer if score2 is higher than this score."""

        # Compare categories first
        categories_diff = self.category - other.category
        if categories_diff:
            return categories_diff

        # Same score, compare the list of cards
        cards1 = self.cards[0:5]
        cards2 = other.cards[0:5]

        # In the traditional italian poker royal flushes are weaker than minimum straight flushes (e.g. 10, 9, 8, 7, A)
        # This is done so you are not mathematically sure to have the strongest hand.
        if self.category == Score.STRAIGHT_FLUSH:
            if Score._straight_is_max(cards1) and Score._straight_is_min(cards2):
                return -1
            elif Score._straight_is_min(cards1) and Score._straight_is_max(cards2):
                return 1

        return Score._cmp_cards(cards1, cards2)

    @staticmethod
    def _cmp_cards(cards1, cards2):
        """Compare two list of cards according to ranks and suits."""
        rank_diff = Score._cmp_ranks(cards1, cards2)
        if rank_diff:
            return rank_diff
        return Score._cmp_suits(cards1, cards2)

    @staticmethod
    def _cmp_ranks(cards1, cards2):
        """Compare two list of cards ranks.
        Returns a negative integer if cards1 < cards2, positive if cards1 > cards2 or 0 if their ranks are identical"""
        for i in range(len(cards1)):
            try:
                rank_diff = cards1[i].rank - cards2[i].rank
                if rank_diff:
                    return rank_diff
            except IndexError:
                # cards1 is longer than cards2
                return 1
        return 0 if len(cards1) == len(cards2) else -1 # cards2 is longer than cards1

    @staticmethod
    def _cmp_suits(cards1, cards2):
        """Compare two list of cards suits.
        Returns a negative integer if cards1 < cards2, positive if cards1 > cards2 or 0 if their suits are identical"""
        for i in range(len(cards1)):
            try:
                suit_diff = cards1[i].suit - cards2[i].suit
                if suit_diff:
                    return suit_diff
            except IndexError:
                # cards1 is longer than cards2
                return 1
        return 0 if len(cards1) == len(cards2) else -1  # cards2 is longer than cards1

    @staticmethod
    def _straight_is_min(straight_sequence):
        return straight_sequence[4].rank == 14

    @staticmethod
    def _straight_is_max(straight_sequence):
        return straight_sequence[0].rank == 14

    def __str__(self):
        return str(self._cards) + " (" + Score.CATEGORIES[self.category] + ")"

    def dto(self):
        return {"category": self.category,
                "cards": [card.dto() for card in self.cards]}
