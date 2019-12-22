class Calculate:
    def __init__(self,conn):
        self.conn=conn

    def get_len(self,language):
        if language == 'python':
            length = len(list(self.conn.select_python()))
            print('python共' + str(length) +'条数据' )
        elif language == 'java':
            length = len(list(self.conn.select_Java()))
            print('Java共' + str(length) + '条数据')
        else:
            length = len(list(self.conn.select_PHP()))
            print('PHP共' + str(length) + '条数据')

        return length

    def avg_sal(self):
        sal = {}
        python_sal = 0
        java_sal = 0
        php_sal = 0

        pythons = self.conn.select_python()
        for python in pythons:
            python_sal = python_sal + int(python['min_price']) + int(python['max_price'])

        python_sal = python_sal / (2 * self.get_len('python'))
        sal['python'] = python_sal

        javas = self.conn.select_Java()
        for java in javas:
            java_sal = java_sal + int(java['min_price']) + int(java['max_price'])

        java_sal = java_sal / (2 * self.get_len('java'))
        sal['java'] = java_sal

        phps = self.conn.select_PHP()
        for php in phps:
            php_sal = php_sal + int(php['min_price']) + int(php['min_price'])

        php_sal = php_sal / (2 * self.get_len('php'))
        sal['php'] = php_sal

        return sal

    def min_price(self,language):
        min_price = {}
        if language == 'python':
            results = self.conn.select_python()
            for result in results:
                if result['area'] in min_price.keys():
                    min_price[result['area']] = int(min_price[result['area']]) + int(result['min_price'])
                else:
                    min_price[result['area']] = int(result['min_price'])

        elif language == 'java':
            results = self.conn.select_Java()
            for result in results:
                if result['area'] in min_price.keys():
                    min_price[result['area']] = int(min_price[result['area']]) + int(result['min_price'])
                else:
                    min_price[result['area']] = int(result['min_price'])

        else:
            results = self.conn.select_PHP()
            for result in results:
                if result['area'] in min_price.keys():
                    min_price[result['area']] = int(min_price[result['area']]) + int(result['min_price'])
                else:
                    min_price[result['area']] = int(result['min_price'])

        return min_price

    def max_price(self,language):
        max_price = {}
        if language == 'python':
            results = self.conn.select_python()
            for result in results:
                if result['area'] in max_price.keys():
                    max_price[result['area']] = int(max_price[result['area']]) + int(result['max_price'])
                else:
                    max_price[result['area']] = int(result['max_price'])

        elif language == 'java':
            results = self.conn.select_Java()
            for result in results:
                if result['area'] in max_price.keys():
                    max_price[result['area']] = int(max_price[result['area']]) + int(result['max_price'])
                else:
                    max_price[result['area']] = int(result['max_price'])

        else:
            results = self.conn.select_PHP()
            for result in results:
                if result['area'] in max_price.keys():
                    max_price[result['area']] = int(max_price[result['area']]) + int(result['max_price'])
                else:
                    max_price[result['area']] = int(result['max_price'])

        return max_price
        
