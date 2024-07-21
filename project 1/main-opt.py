import pickle
import sys

def solve_instance(n, c, pt):
    # preprocess
    sum_x = [0]
    sum_y = [0]
    sum_xy = [0]
    sum_x2 = [0]
    sum_y2 = [0]
    for p in pt:
        sum_x.append(sum_x[-1] + p[0])
        sum_y.append(sum_y[-1] + p[1])
        sum_xy.append(sum_xy[-1] + p[0] * p[1])
        sum_x2.append(sum_x2[-1] + p[0] * p[0])
        sum_y2.append(sum_y2[-1] + p[1] * p[1])
        
    def epsilon(start, end):
        if start == end:
            return 0
            
        dxy = sum_xy[end + 1] - sum_xy[start]
        dx = sum_x[end + 1] - sum_x[start]
        dy = sum_y[end + 1] - sum_y[start]
        dx2 = sum_x2[end + 1] - sum_x2[start]
        dy2 = sum_y2[end + 1] - sum_y2[start]
        m = end - start + 1
        
        if abs(m * dx2 - dx * dx) < 1e-12:
            return 0
        a = (m * dxy - dx * dy) / (m * dx2 - dx * dx)
        b = (dy - a * dx) / m
        # error term Error(L, P)
        return dy2 + a * a * dx2 + m * b * b - 2 * a * dxy + 2 * a * b * dx - 2 * b * dy
        
    dp   = [ None for i in range(n + 1) ]
    bk   = [ None for i in range(n + 1) ]
    dp[0] = 0
    for i in range(n):
        dp[i + 1] = epsilon(0, i) + c
        bk[i + 1] = -1
        
        for j in range(0, i):
            x = epsilon(j, i)
            if dp[j] + x + c < dp[i + 1]:
                dp[i + 1] = dp[j] + x + c
                bk[i + 1] = j - 1
    opt = dp[n]
    k = 0
    q = n - 1
    lp = []
    while q >= 0:
        k += 1
        lp.append(q)
        q = bk[q + 1]
    return k, list(reversed(lp)), opt
        
def main(inputfile, outputfile):
    inp = pickle.load(open(inputfile, 'rb'))
    oup = {
        'k_list': [],
        'last_points_list': [],
        'OPT_list': [],
    }
    for i, n in enumerate(inp['n_list']):
        print(f"{i} / {len(inp['n_list'])} {n}")
        k, lps, opt = solve_instance(n, inp['C_list'][i], list(zip(inp['x_list'][i], inp['y_list'][i])))
        oup['k_list'].append(k)
        oup['last_points_list'].append(lps)
        oup['OPT_list'].append(opt)
    print(oup)
      
    with open(outputfile, 'wb') as f:
        pickle.dump(oup, f)

if __name__ == '__main__':
    main(*sys.argv[1:])