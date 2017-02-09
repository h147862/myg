# class Demo:
#     x = 0
#
#     def __init__(self, i):
#         self.i = i
#         self.x = i
#
#
#
#
#     def __str__(self):
#         return str(self.i)
#
#     def hello(self):
#         print("hello", self.i)
#
#
#     def getX(self):
#         return self.x
#
#     def setX(self,num):
#         self.x = num
#
#
# class SubDemo(Demo):
#     pass
#
#
#
#
# t = Demo(1234)
#
#
# a = SubDemo(1234)
# a.hello()
# b = SubDemo(5678)
# a.setX(1000)
# print(a.getX())
#
# b.hello()
# print(b.getX())
#
#
#
#
#
#
#
#
#
#
# c = SubDemo(9012)
# c.hello()
# print(c.getX())
# d = SubDemo(3456)
# d.hello()
# print(b.getX())
# e = SubDemo(7890)
# e.hello()
# print(b.getX())

# a = [1,2,3,4,8,6,7]
# del a[5:]
#
# print a


# class PassByReference:
#     def __init__(self,p):
#         self.ary = p
#     def Change(self, var):
#         s1 = var[0]
#         s2 = var[1]
#         var[0] = s2
#         var[1] = s1
#         # print var
#         # print self.ary
#
#     def triger(self):
#         self.Change(self.ary)
#
#
# a = PassByReference([4,5,6])
#
# print a.ary
#
# a.triger()
# print a.ary

#
#
# def test(a):
#     s1 = a[0]
#     s2 = a[1]
#     a[0] = s2
#     a[1] = s1
#
# b = [4,5,6]
#
# test(b)
#
# print b

#
# import matplotlib.pyplot
#
#
# x = [1,2,3,4]
# y = [3,4,8,6]
#
# matplotlib.pyplot.scatter(x,y)
#
# matplotlib.pyplot.show()


b = [1,2,3,4,5]


del b[:3]





print b



