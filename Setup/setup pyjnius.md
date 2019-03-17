Getting JAVA_HOME KeyError while importing autoclass?
  1. Open ~/.bashrc file
  2. copy this line:
      export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 export 
      PATH=$JAVA_HOME/bin:$PATH 
      (path / or java version may differ, make sure to check it before copying)
  3. save the file and log out
  
Work around: 
    import os
    try:
         from jnius import autoclass

    except KeyError:
         os.environ['JDK_HOME'] = "/usr/lib/jvm/java-1.8.0-openjdk-amd64"
         os.environ['JAVA_HOME'] = "/usr/lib/jvm/java-1.8.0-openjdk-amd64"
         from jnius import autoclass
