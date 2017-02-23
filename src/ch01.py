# -*- coding: utf8 -*-

import scipy as sp

data_path = '../ch01/data/web_traffic.tsv'

# 预处理数据
data = sp.genfromtxt(data_path, delimiter="\t")
x = data[:, 0]
y = data[:, 1]
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

# 通过图像观察数据
import matplotlib.pyplot as plt
plt1 = plt.subplot(211)
plt2 = plt.subplot(212)


def plt_org(p, x, y):
    p.scatter(x, y, s=10)
    # p.title("Web traffic over the last month")
    # p.xlabel("Time")
    # p.ylabel("Hits/Hour")
    # plt.xticks([w*7*24 for w in range(10)], ['week %i' % w for w in range(10)])
    p.set_xticks([w*7*24 for w in range(10)])
    p.set_xticklabels(['week %i' % w for w in range(10)])
    p.autoscale(tight=True)
    p.grid(True, linestyle='-', color='0.75')

plt_org(plt1, x, y)
# plt.show()


# ==================================
# 第一个模型: 一阶多项式，通过 polyfit 求出对于多项式的参数(误差最小)
fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
print "Model parameters: %s" % fp1  # 模型对于的参数
print "the error of approximation: %s" % residuals
# Model parameters: [   2.59619213  989.02487106]
# the error of approximation: [  3.17389767e+08]
# 即对于一阶多项式，最接近的模型函数为: fx = 2.59 * x + 989

# 使用 poly1d() 构建函数模型
f1 = sp.poly1d(fp1)


def error(f, x, y):
    """误差函数"""
    return sp.sum((f(x) - y) ** 2)

print 'f1 error: %s' % error(f1, x, y)

# 画出模型 f1
fx = sp.linspace(0, x[-1], 1000)
plt1.plot(fx, f1(fx), linewidth=4)
# plt.legend(["d=%i" % f1.order], loc="upper left")
# plt.show()


# ====================================
# 第二个模型: 二阶多项式
fp2 = sp.polyfit(x, y, 2)
print "fp2: %s" % fp2
f2 = sp.poly1d(fp2)
print 'f2 error: %s' % error(f2, x, y)
plt1.plot(fx, f2(fx), linewidth=4)
# plt.legend(["d=%i" % f2.order], loc="upper left")
# plt.show()

# ===================================
# 高阶多项式
fp3 = sp.polyfit(x, y, 3)
print "fp3: %s" % fp3
f3 = sp.poly1d(fp3)
print 'f3 error: %s' % error(f3, x, y)
plt1.plot(fx, f3(fx), linewidth=4)

fp10 = sp.polyfit(x, y, 10)
print "fp10: %s" % fp10
f10 = sp.poly1d(fp10)
print 'f10 error: %s' % error(f10, x, y)
plt1.plot(fx, f10(fx), linewidth=4)


fp53 = sp.polyfit(x, y, 53)
print "fp53: %s" % fp53
f53 = sp.poly1d(fp53)
print 'f53 error: %s' % error(f53, x, y)
plt1.plot(fx, f53(fx), linewidth=4)
plt1.legend(["d=%i" % i for i in [f1.order, f2.order, f3.order, f10.order, f53.order]], loc="upper left")
# plt1.show()


# ==================================
# 通过观察，发现多项式的模型并不好，回来重新分析原始数据
# 发现在 3.5 week 的时候有个较大变化
inflection = 3.5 * 7 * 24
xa = x[:inflection]
ya = y[:inflection]
xb = x[inflection:]
yb = y[inflection:]

fa = sp.poly1d(sp.polyfit(xa, ya, 1))
fb = sp.poly1d(sp.polyfit(xb, yb, 1))

fa_error = error(fa, xa, ya)
fb_error = error(fb, xb, yb)
print "Errors: %s" % (fa_error + fb_error)
plt_org(plt2, x, y)
plt2.plot(fx, fa(fx), linewidth=4)
fx_b = fx[fb(fx) > 0]
plt2.plot(fx_b, fb(fx_b), linewidth=4)

plt.show()
