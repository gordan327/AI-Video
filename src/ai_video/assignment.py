class GreedyAssignment:
    """Greedy Assignment"""

    def assign(
        self,
        matrix,
    ):

        pairs = []

        used_rows = set()
        used_cols = set()

        while True:

            best_score = -1
            best_pair = None

            for r, row in enumerate(matrix):

                if r in used_rows:
                    continue

                for c, score in enumerate(row):

                    if c in used_cols:
                        continue

                    if score > best_score:

                        best_score = score
                        best_pair = (r, c)

            if best_pair is None:
                break

            used_rows.add(best_pair[0])
            used_cols.add(best_pair[1])

            pairs.append(best_pair)

        return pairs