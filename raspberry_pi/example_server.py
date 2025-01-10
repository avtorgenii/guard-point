from bottle import post, request, run
@post('/enterance')
def do_something():
    print(request.json)

if __name__ == '__main__':
    run(host='localhost',port = 8080, debug = True)
