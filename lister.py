class Attr_tree:
    def __str__(self):
        self.__class_dict=dict()
        return 'экземпляр принадлежит {0}, адресс в памяти {1}\nаттрибуты экземпляра:\n{2}аттрибуты класса: {3}'.format(self.__class__.__name__,
                                                                                                                     id(self.__class__),
                                                                                                                     self.__ob_attr(self,0),
                                                                                                                     self.__cl_attr(self.__class__,4))

    
    def __ob_attr(self,ob,dnum):
        dot='.'*(dnum+4)
        myattr=''
        for e in sorted(ob.__dict__):
            if e.startswith('__') and e.endswith(''):
                myattr+=dot+f'{e} = встроеный метод\n'
            else:
                myattr+=dot+'{0} = {1}\n'.format(e,getattr(ob,e))
        return myattr
                
    # обратное сложение
    def __cl_attr(self,baseClass,n):
        pl='-'*n
        if baseClass in self.__class_dict:
            return '\n{0} имя класса {1}, адрес в памяти {2}'.format(pl,baseClass.__name__, id(baseClass))
        else:
            self.__class_dict[baseClass]=True
            bypass=(self.__cl_attr(c,n*2) for c in baseClass.__bases__)# возврат строки в кортеж 
            return '\n{0} имя класса {1}, адрес в памяти {2}, аттрибуты:\n{3}{4}\n'.format(
                pl,
                baseClass.__name__,
                id(baseClass),
                self.__ob_attr(baseClass,n),
                ''.join(bypass))   


# a(b,c)
# b(object)
# c(e,object)
# e(object)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++
class one:
    def __init__(self):
            self.one=1

class two(one):
    def __init__(self):
        self.two=2
        one.__init__(self)

class pHello:
    def say(self):
        return 'hello'

class three(Attr_tree,two,pHello):
        three=3

if __name__=='__main__':
    
    a=three()
    print(a)
    input('')

        
