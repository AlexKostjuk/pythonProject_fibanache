import redis

r_cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

def redis_cache(func):
    def wrapper(self, n):
        if r_cache.exists(n):
            ret = r_cache.get(n)
            print(f'from: {ret}')
            return int(ret)
        else:
            result = func(self, n)
            r_cache.set(n, result, ex=10)
            print(f'calculate : {result}')
            return result
    return wrapper

class Fib:
    def fibonacci(self, n):
        if n <= 1:
            return n
        else:
            return self.fibonacci(n-1) + self.fibonacci(n-2)

    @redis_cache
    def clir_fibonacci(self, n):
        return self.fibonacci(n)

    def calk_fibonacci(self, n):
        fib = []
        for i in range(n):
            fib.append(self.clir_fibonacci(i))
        return fib

f = Fib()
print(f.calk_fibonacci(10))
