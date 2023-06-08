import time

class log:
    def __init__(self,task) -> None:
        self.st = float(time.time())
        self.task = task
        with open('log.text','a',newline='',encoding='utf8') as f:
            self.ed = float(time.time())
            f.write(f'{self.task} is start at {self.st}s\n')

    def over_p2(self,type):
        with open('log.text','a',newline='',encoding='utf8') as f:
            self.ed = float(time.time())
            f.write(f'aid:{self.task} is '+type+f' in {self.ed-self.st}s\n')

    def over_p3(self,type):
        with open('log.text','a',newline='',encoding='utf8') as f:
            self.ed = float(time.time())
            f.write(f'uid:{self.task} is '+type+f' in {self.ed-self.st}s\n')

if __name__ == "__main__":
    log1 = log()
    time.sleep(1)
    log1.over_p2(12345,'err')
    time.sleep(1)
    log1.over_p3(1212,'ok')
