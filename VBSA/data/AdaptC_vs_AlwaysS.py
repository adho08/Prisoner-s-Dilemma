payoffs_A = []

def payoff(x, y, c=0.5) -> tuple[float, float]:

    v1 = y - c*x + c
    v2 = x - c*y + c

    return round(v1, 2), v2

def i(p_A, p_R, r, print_r=None):
    global payoffs_A
    if r == 1:
        investm = 1.0
    elif print_r != None:
        investm = max(0.0, min(1.0, i(p_A, p_R, r-1, print_r-1)[0] + s(p_A, p_R, r)))
    else:
        investm = max(0.0, min(1.0, i(p_A, p_R, r-1)[0] + s(p_A, p_R, r)))
    p,_ = payoff(investm, p_R/10)
    if print_r:
        payoffs_A.append(p)
        print(f"{r}. round:\t {investm:.2f},\t {p}")
    return investm, 2, p

def s(p_A, p_R, r):
    s = p_A/5 * (p_R / 10 - i(p_A, p_R, r-1)[0])
    return s

def print_i(p_A, p_R, r):
    i(p_A, p_R, r, r)

print_i(2, 0, 20)

print(sum(payoffs_A))
