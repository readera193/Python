class Test():
    PIDs = []
    def __init__(self):
        self.PIDs.append(8)

def main():
    for i in range(2):
        Test()
    print(Test.PIDs)

if __name__ == '__main__':
    main()