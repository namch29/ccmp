import os.path,subprocess
from subprocess import STDOUT,PIPE

def compile_java(java_file):
    subprocess.check_call(['javac', java_file])

def execute_java(java_file, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin)
    print ('This was "' + stdout + '"')
    
def execute_java2(java_file):
    java_class,ext = os.path.splitext(java_file)
    #print java_class
    #print ext
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    print ('This was "' + stdout + '"')


def execute_jar(jar_file):
    agr1 = 'test'
    agr2 = 'data-abilene'
    cmd = ['java', '-jar', jar_file, agr1, agr2]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    print ('This was "' + stdout + '"')
 
def main():
	
	file_name = 'NFVReliable.jar'
	execute_jar(file_name)
	
    
main()
#java -jar NFVReliable.jar test data-abilene


