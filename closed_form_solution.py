"""
Closed-Form Solution for the Probability of Stopping

Problem:
    Given trials that go on for w time periods with probability of success p,
    the trials will end (failure) if there aren't n successive successes after
    a failure, or if a failure comes in a j > w-n time period.

    What is the probability of the trials ending?

Solution:
    P(failure) = 1 - sum_{f=0}^{f_max} C(w - f*n, f) * p^(w-f) * (1-p)^f

    where f_max = floor(w / (n+1))

Derivation:
    A "success" sequence (trials survive all w periods) with exactly f failures
    has the block structure:

        S...S  F  S...S  F  ...  F  S...S
        (s_0)     (s_1)          (s_f)

    where s_0 >= 0 and s_1, ..., s_f >= n (each F must be followed by at least
    n consecutive S's). The total length constraint is:

        s_0 + s_1 + ... + s_f + f = w

    Substituting s_i' = s_i - n for i >= 1:

        s_0 + s_1' + ... + s_f' = w - f - f*n = w - f*(n+1)

    The number of non-negative integer solutions (stars and bars) is:

        C(w - f*(n+1) + f, f) = C(w - f*n, f)

    Summing over all valid f from 0 to f_max gives the total probability of
    success, and P(failure) = 1 - P(success).

Complexity: O(w/n) vs O(exponential) for the brute-force permutation approach.
"""

import math


def p_failure(w: int, n: int, p: float) -> float:
    """
    Compute the probability of trials ending (failure) using the closed-form solution.

    Parameters:
        w: Number of time periods
        n: Number of successive successes required after a failure
        p: Probability of success in each trial

    Returns:
        Probability of the trials ending (failure)
    """
    q = 1 - p
    f_max = w // (n + 1)
    p_success = 0.0
    for f in range(f_max + 1):
        binom_top = w - f * n
        if binom_top < f:
            break
        p_success += math.comb(binom_top, f) * (p ** (w - f)) * (q ** f)
    return 1 - p_success


if __name__ == "__main__":
    # Example parameters (same as the brute-force script)
    w = 15
    n = 6
    p = 3 / 8

    result = p_failure(w, n, p)
    print(f"Parameters: w={w}, n={n}, p={p}")
    print(f"P(failure) = {result}")
    print(f"P(success) = {1 - result}")
