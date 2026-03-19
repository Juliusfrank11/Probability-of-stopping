# Probability of Stopping

## Problem

Find a closed-form solution for the following probability:

> Given trials that go on for **w** time periods with probability of success **p**, and that the trials will end if there aren't **n** successive successes after a failure, or if a failure comes in a **j > w - n** time period, what is the probability of the trials ending?

## Solution

### Closed Form

$$P(\text{failure}) = 1 - \sum_{f=0}^{f_{\max}} \binom{w - fn}{f} \cdot p^{w-f} \cdot (1-p)^f$$

where:

$$f_{\max} = \left\lfloor \frac{w}{n+1} \right\rfloor$$

### Derivation

A "success" sequence — one where the trials survive all **w** periods — with exactly **f** failures has the block structure:

$$\underbrace{S \cdots S}\_{s_0} \; F \; \underbrace{S \cdots S}\_{s_1} \; F \; \cdots \; F \; \underbrace{S \cdots S}\_{s_f}$$

The constraints are:
- **s₀ ≥ 0** (leading successes are optional)
- **s₁, ..., sₓ ≥ n** (each failure must be followed by at least n consecutive successes)
- The sequence must end in S
- The last failure must occur at or before position w - n - 1 (0-indexed)

The total length constraint gives us:

$$s_0 + s_1 + \cdots + s_f + f = w$$

Substituting **s'ᵢ = sᵢ - n** for **i ≥ 1** (absorbing the minimum n successes required after each failure):

$$s_0 + s'_1 + \cdots + s'_f = w - f - fn = w - f(n+1)$$

The **-f** accounts for the f failure tokens themselves occupying positions, and the **-fn** accounts for the n mandatory successes after each failure.

By stars and bars, the number of non-negative integer solutions with f+1 variables is:

$$\binom{w - f(n+1) + f}{f} = \binom{w - fn}{f}$$

Each valid sequence with f failures occurs with probability **p^(w-f) · (1-p)^f**. Summing over all valid f gives the total probability of success, and **P(failure) = 1 - P(success)**.

### Maximum Number of Failures

The maximum f is bounded by requiring the stars count to be non-negative:

$$w - f(n+1) \geq 0 \implies f \leq \frac{w}{n+1}$$

Since f must be an integer: **f_max = ⌊w / (n+1)⌋**.

Note: An equivalent form derived from the geometric constraint on where the last failure can sit is **f_max = 1 + ⌊(w - n - 1) / (n+1)⌋**. These are algebraically identical via the standard floor identity.

## Files

| File | Description |
|------|-------------|
| `probability-of-stopping.py` | Original brute-force solution that enumerates all valid permutations |
| `closed_form_solution.py` | O(w/n) closed-form solution |

## Usage

```bash
# Closed-form solution (fast)
python closed_form_solution.py

# Brute-force verification (slow for large w)
python probability-of-stopping.py
```

Both scripts use **w=15, n=6, p=3/8** as default parameters and should output the same probability of failure: **≈ 0.9999900763686753**.

## Complexity

- **Brute-force** (`probability-of-stopping.py`): Generates all distinct permutations — exponential in w.
- **Closed-form** (`closed_form_solution.py`): O(w/n) — a single loop over at most ⌊w/(n+1)⌋ terms.
