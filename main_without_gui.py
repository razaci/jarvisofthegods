from commands import handle
if __name__ == '__main__':
    print('Jarvis console. Type help or exit.')
    while True:
        try: query=input('You> ')
        except (EOFError, KeyboardInterrupt): break
        if query.strip().lower() in ('exit','quit'):break
        try:print(handle(query))
        except Exception as exc:print('Error:',exc)
