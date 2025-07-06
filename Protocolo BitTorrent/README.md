# Utilização do protocolo bittorrent
O protocolo BitTorrent é utilizado para troca de arquivos de forma distribuída e a presente implementação visa simular de forma aproximada como que esse protocolo funciona "por baixo dos panos".

Comando para leecher e seeder: 
Exemplo genérico: <python_path> <nome_do_executavel>.py <nome_do_arquivo_alvo>.<extensao_do_arquivo_alvo> --tracker <trackerIP:trackerPORTA> --listen-port <porta_em_que_será_executado_o_peer>
Exemplo real: C:/Python312/python.exe peer.py teste2.pdf --tracker 10.20.180.141:10000 --listen-port 6001

# PASSOS
1) Iniciar o tracker (apenas executar o arquivo tracker.py)
2) Iniciar o seeder (comando acima)
3) Iniciar um ou mais leechers (que poderão se tornar seeder posteriormente) (comando acima)

# OBSERVAÇÕES:
1) A comunicação dos peers com o tracker é via UDP, então é necessário verificar se o firewall entre eles está liberando a porta tanto do tracker quanto dos peers para receber UDP.
2) A comunicação dos peers entre si ocorre via TCP, então precisa avaliar se estão conseguindo trocar pacotes e se o handshake ocorre sem erros. 
