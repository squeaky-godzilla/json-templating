d = {
    "a": "b",
    "b": "c",
    "c": "a"
  }

def resolve(d):

    to_resolve = d
    resolved_d = d
    
    # while len(to_resolve.keys()) > 0:
    for variable in to_resolve.keys():
        # print(variable)
        for key, value in resolved_d.items():
            if variable in value:
                if variable == to_resolve[variable]:
                    print("cyclical reference")
                else:
                    resolved_d[key] = value.replace(variable, to_resolve[variable])

                # print("resolved_d", resolved_d)
            else:
                pass
        # to_resolve.pop(variable)
        # print("to_resolve: ", to_resolve)
              

    return resolved_d

print(resolve(d))
import pdb; pdb.set_trace()