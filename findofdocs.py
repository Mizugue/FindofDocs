import requests
import argparse
import sys
import time
import pyautogui
import colorama



def argumentos(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='Digite o alvo', required=True)
    parser.add_argument('-a', help='Vulnerabilidades de listagem de diretórios', action='store_true')
    parser.add_argument('-b', help=' Arquivos de configuração expostos', action='store_true')
    parser.add_argument('-c', help='Arquivos de banco de dados expostos', action='store_true')
    parser.add_argument('-d', help='Encontrar relacionados WordPress', action='store_true')
    parser.add_argument('-e', help='Arquivos de log expostos', action='store_true')
    parser.add_argument('-f', help='Backup e arquivos antigos', action='store_true')
    parser.add_argument('-g', help='Páginas de login', action='store_true')
    parser.add_argument('-v', help='Erros de SQL', action='store_true')
    parser.add_argument('-i', help='Documentos expostos publicamente', action='store_true')
    parser.add_argument('-j', help='phpinfo()', action='store_true')
    parser.add_argument('-k', help='Encontrar backdoors', action='store_true')
    parser.add_argument('-l', help='Arquivos de instalação/configuração', action='store_true')
    parser.add_argument('-m', help='Open redirects', action='store_true')
    parser.add_argument('-n', help='Apache STRUTS RCE', action='store_true')
    parser.add_argument('-o', help='Encontre entradas no Pastebin', action='store_true')
    parser.add_argument('-q', help='Arquivos confidenciais .htaccess', action='store_true')
    parser.add_argument('-r', help='Encontrar subdomínios', action='store_true')
    parser.add_argument('-s', help='Encontrar sub-subdomínios', action='store_true')
    parser.add_argument('-t', help='Encontrar relacionados WordPress #2', action='store_true')
    parser.add_argument('-y', help='Encontre o arquivo .SWF (Google)', action='store_true')
    parser.add_argument('-devil', help='Wordlist com diversas docs! ')
    parser.add_argument('-all', help='Todas as opcoes', action='store_true')
    parser.add_argument('-help', action='help', help='Mostra todos os argumentos')
    args = parser.parse_args(argv)

    global target
    target = args.u

    return args



def getdoc(args):
    global adds
    adds = []
    if args.all:
        for name, value in vars(args).items():
            if isinstance(value, bool) and name != 'all':
                setattr(args, name, True)
    if args.a:
        add = ' intitle:index.of'
        adds.append(add)
    if args.b:
        add = ' ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini'
        adds.append(add)
    if args.c:
        add = ' ext:sql | ext:dbf | ext:mdb'
        adds.append(add)
    if args.d:
        add = ' inurl:wp- | inurl:wp-content | inurl:plugins | inurl:uploads | inurl:themes | inurl:download'
        adds.append(add)
    if args.e:
        add = ' ext:log'
        adds.append(add)
    if args.f:
        add = ' ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup'
        adds.append(add)
    if args.g:
        add = ' inurl:login'
        adds.append(add)
    if args.v:
        add = ' intext:"sql syntax near" | intext:"syntax error has occurred" | intext:"incorrect syntax near" | intext:"unexpected end of SQL command" | intext:"Warning: mysql_connect()" | intext:"Warning: mysql_query()" | intext:"Warning: pg_connect()"'
        adds.append(add)
    if args.i:
        add = ' ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv'
        adds.append(add)
    if args.j:
        add = ' ext:php intitle:phpinfo "published by the PHP Group"'
        adds.append(add)
    if args.k:
        add = ' inurl:shell | inurl:backdoor | inurl:wso | inurl:cmd | shadow | passwd | boot.ini | inurl:backdoor'
        adds.append(add)
    if args.l:
        add = ' inurl:readme | inurl:license | inurl:install | inurl:setup | inurl:config'
        adds.append(add)
    if args.m:
        add = ' inurl:redir | inurl:url | inurl:redirect | inurl:return | inurl:src=http | inurl:r=http'
        adds.append(add)
    if args.n:
        add = ' ext:action | ext:struts | ext:do'
        adds.append(add)
    if args.o:
        add = ' site:pastebin.com'
        adds.append(add)
    if args.q:
        add = ' inurl:"/phpinfo.php" | inurl:".htaccess" | inurl:"/.git"  -github'
        adds.append(add)
    if args.r:
        add = ' *.'
        adds.append(add)
    if args.s:
        add = ' *.*.'
        adds.append(add)
    if args.t:
        add = ' inurl:wp-content | inurl:wp-includes'
        adds.append(add)
    if args.y:
        add = ' inurl: ext:swf'
        adds.append(add)
    if args.devil:
        try:
            with open(args.devil, 'r', encoding="utf-8") as f:
                for l in f:
                    add = ' ' + l
                    #adds.append(' ' + l.strip())
                    adds.append(add)
        except FileNotFoundError:
            print(colorama.Fore.LIGHTRED_EX + "Erro: Arquivo wordlist não encontrado.")
            sys.exit(1)
        except PermissionError:
            print(colorama.Fore.LIGHTRED_EX + "Erro: Sem permissão para acessar o arquivo wordlist.")
            sys.exit(1)




    if adds.__len__() > 1:
        return adds
    elif adds.__len__() == 1:
        return add
    else:
        return print('Digite algum argumento'), exit()


def datadocs():
    global target
    global url
    global robo
    global erro

    try:
        requests.get(target)
    except:
        return print('Talvez voce tenha digitado a url incorretamente, já que não conseguimos nem estabelecer uma conexao'), exit()

    docs = 'https://www.google.com/search?q='
    site = 'site:' + target
    erro = 'não encontrou nenhum documento correspondente.'
    robo = 'Our systems have detected unusual traffic from your computer network'
    url = docs + site

def start():
    exitos = []
    barrados = []
    global url
    save = url
    add = getdoc(args)

    if type(add) == list:
        for i in add:
            pyautogui.sleep(5)
            url = save
            url = url + i
            r = requests.get(url)
            if erro in r.text:
                print(colorama.Fore.RED + f"        Não encontramos nada!   ")
                print(f'--->   {url}   ')
                print('')
            elif robo in r.text:
                while robo in r.text:
                    r = requests.get(url)
                    tempo_decorrido = time.time()
                    if tempo_decorrido > 5:
                        print(colorama.Fore.YELLOW + "     Nao conseguimos bypassar o reCAPTCHA. Logo, pulando a url!")
                        print(f'--->   {url}   ')
                        print('')
                        barrados.append(url)
                        break
            else:
                print(colorama.Fore.GREEN + f'    Encontramos algo!   ')
                print(f'--->   {url}   ')
                print('')
                exitos.append(url)
    else:
        url = save
        url = url + add
        r = requests.get(url)
        if erro in r.text:
            print(colorama.Fore.RED + f"        Não encontramos nada!   ")
            print(f'--->   {url}   ')
            print('')
        elif robo in r.text:
            while robo in r.text:
                r = requests.get(url)
                tempo_decorrido = time.time()
                if tempo_decorrido > 8:
                    print(colorama.Fore.YELLOW + "     Nao conseguimos bypassar o reCAPTCHA. Logo, pulando os docs!")
                    print(f'--->   {url}   ')
                    print('')
                    break
        else:
            print(colorama.Fore.GREEN + f'    Encontramos algo!   ')
            print(f'--->   {url}   ')
            print('')


    if type(add) == list:
        print('')
        print(colorama.Fore.LIGHTGREEN_EX + "DOCS COM EXITO: \n")
        for i in exitos:
            print(i)
        print(colorama.Fore.LIGHTYELLOW_EXY + "DOCS BARRADAS PELO RECAPTCHA \n")
        for i in barrados:
            print(i)



if __name__ == "__main__":
    colorama.init()
    try:
        args = argumentos(sys.argv[1:])
        data = datadocs()
        getdoc(args)
        start()
    finally:
        colorama.deinit()






