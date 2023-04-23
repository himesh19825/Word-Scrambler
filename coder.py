import random
class Myclass:
    i = 0
    wk=""
    val=0
    def __init__(self):
        self.lives=0
        self.val_score=0

    l= ['ant', 'apple', 'dog', 'ice', 'cone','dwaraka','australia','sahara','warlock','wednesday','tiger','biryani','python','conjuring','historian','dolphin','joules','hint','pizza']
    h= ['insect', 'fruit', 'Pet animal', 'cool', 'shape','Under water city','Island continent','Desert','Witchcraft','A day and a series','Animal','Hyderabad','Snake','Movie','Museum','A mamal','A unit of Measurement','Hint','Food']
    def fun(self):
        obj=Myclass()
        global l
        l=obj.l
        word=random.choice(l)
        global i
        i=l.index(word)
        self.wk=word
        return self.scramb(word),self.h[i]

    def scramb(self,word):
        lst=list(word)
        random.shuffle(lst)
        w=''.join(lst)
        return w

    def validat(self,word="",tosend="",val_score=0,lives=0):#val_score=0
        # print(word)
        # obj=Myclass()
        # ind=obj.i
        # print(tosend)
        if word==tosend:
            self.val=val_score+1
            self.lives=lives
            # print(self.val)
        elif word=="":
            # global lives
            pass
        else:
            self.lives=lives-1
            self.val=val_score
            # print(self.lives)
        return self.lives,self.val