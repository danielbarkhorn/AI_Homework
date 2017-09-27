import resolve
import engine

print(resolve.resolve(['or', 'a', 'b'], ['not', 'b']))
print(resolve.resolve(['or', ['not', 'a'], ['not', 'b']], 'a'))
print(resolve.resolve(['or', 'a', ['not', 'b']], ['not', 'a']))
