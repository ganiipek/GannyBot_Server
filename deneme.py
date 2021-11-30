from pancakeswap import PancakeSwap
from datetime import datetime

if __name__ == "__main__":
    ps = PancakeSwap()
    ps.startWeb3()

    while True:
        print("\n")
        time1 = datetime.now()
        print(ps.calcTokenPrice("0x9130990dd16ed8be8be63e46cad305c2c339dac9"))
        time2 = datetime.now()
        print("diff: " + str(time2 - time1))