from jnius import autoclass
from jnius import JavaClass, MetaJavaClass

#Stack = autoclass('java.util.Stack')
#stack = Stack()
#stack.push('hello')
#stack.push('world')

#print stack.pop() # --> 'world'
#print stack.pop() # --> 'hello'

#java_resource_jar_path = "/path/to/jar/directory"
#jnius_config.set_classpath(java_resource_jar_path)

#from jnius import autoclass
## from jnius import JavaException  
## You might have to import JavaException if your class happens to throw exceptions

#TheJavaClass = autoclass(path.in.the.jar.file.to.class) # No ".class", no parentheses
#python_instance_of_the_Java_class = TheJavaClass()

Stack = autoclass('A')
#stack = Stack()
Stack.name()
Stack.main()
