def checklib(lib, path):
    path.append(lib)
    visited[lib] = True
    if libs.__contains__(lib):
        print(*path[::-1])
    if dependencies.get(lib) is not None:
        for dep in dependencies[lib]:
            if not visited[dep]:
                checklib(dep, path)
    path.pop()
    visited[lib] = False


vulnerable = set(input().split())
libs = set(input().split())
dependencies = {}
visited = {}
visited.update(dict.fromkeys(vulnerable, False))
visited.update(dict.fromkeys(libs, False))

while True:
    try:
        lib = input()
    except EOFError:
        break
    if len(lib) == 0:
        continue
    lib = lib.split()
    visited.update(dict.fromkeys(lib, False))
    for dep_lib in lib[1:]:
        if dependencies.get(dep_lib) is None:
            dependencies.update({dep_lib: {lib[0]}})
        else:
            dependencies.get(dep_lib).add(lib[0])

for lib in vulnerable:
    checklib(lib, [])

