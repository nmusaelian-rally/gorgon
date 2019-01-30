import os
import yaml
# take an file argument which represents the name of a file containing app.yaml valid syntax
# if such a file exists by that name in the current directory (or subdirs?)
# open up the file, attempt to JSON'ify it, look for the env_variables section
# and "load-up" the environment with the elements under that section


class AppSettings:
    @staticmethod
    def loadEnvironment(filename):
        if os.path.exists(filename):
            with open(filename, "r") as af:
                try:
                    d = yaml.load(af.read())
                    if 'env_variables' in d:
                        for name, value in d['env_variables'].items():
                            #print("%s    %s" % (name, value))
                            os.environ[name] =  str(value)
                except Exception as ex:
                    print(ex)
                    pass
        else:
            pass
            #print("no such file named '%s' in the cwd" % filename)