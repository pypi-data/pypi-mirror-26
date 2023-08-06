# Totalvoice-python
Cliente em Python para API da Totalvoice

[![Build Status](https://travis-ci.org/totalvoice/totalvoice-python.svg?branch=master)](https://travis-ci.org/totalvoice/totalvoice-python)

## Pré requisitos

```
$ pip install totalvoice
```

## Como utilizar (how to)

Segue abaixo a forma de utilização dos métodos da API da totalvoice!

### Chamadas
Módulo responsável por criação de chamadas, relatórios de chamadas, url da gravação, etc.


```python
from totalvoice.cliente import Cliente

cliente = Cliente("SEU_TOKEN", 'HOST') #ex: api.totalvoice.com.br

#Cria chamada
numero_origem = "48999999999"
numero_destino = "48900000000"
response = cliente.chamada.enviar(numero_origem, numero_destino)
print(response)

#Get chamada
id = "1958"
response = cliente.chamada.get_by_id(id)
print(response)

#Get URL da chamada
id = "1958"
response = cliente.chamada.get_gravacao_chamada(id) 
print(response)

#Relatório de chamada
data_inicio = "2016-03-30T17:15:59-03:00"
data_fim = "2016-03-30T17:15:59-03:00"
response = cliente.chamada.get_relatorio(data_inicio, data_fim)
print(response)

#Escutar chamada (BETA)
id_chamada = "1958"
numero = "48999999999"
modo = 1 #1=escuta, 2=sussurro, 3=conferência.
response = cliente.chamada.escuta_chamada(id_chamada, numero, modo)
print(response)

#Deletar
id = "1958"
response = cliente.chamada.deletar(id)
print(response)


```

### SMS
Módulo responsável por criação de SMS, relatórios.

```python
from totalvoice.cliente import Cliente

cliente = Cliente("SEU_TOKEN", 'HOST') #ex: api.totalvoice.com.br

#Cria sms
numero_destino = "48999999999"
mensagem = "teste envio sms"
response = cliente.sms.enviar(numero_destino, mensagem)
print(response)

#Get sms
id = "1958"
response = cliente.sms.get_by_id(id)
print(response)

#Relatório de sms
data_inicio = "2016-03-30T17:15:59-03:00"
data_fim = "2016-03-30T17:15:59-03:00"
response = cliente.sms.get_relatorio(data_inicio, data_fim)
print(response)

```

### Audio
Módulo responsável por criação de Audios.

```python
from totalvoice.cliente import Cliente

cliente = Cliente("SEU_TOKEN", 'HOST') #ex: api.totalvoice.com.br

#Cria audio
numero = "48999999999"
url_audio = "http://fooo.bar"
response = cliente.audio.enviar(numero, url_audio)
print(response)

#Get audio
id = "1958"
response = cliente.audio.get_by_id(id)
print(response)

#Relatório de audio
data_inicio = "2016-03-30T17:15:59-03:00"
data_fim = "2016-03-30T17:15:59-03:00"
response = cliente.audio.get_relatorio(data_inicio, data_fim)
print(response)

```

### TTS
Módulo responsável por criação de Audios.

```python
from totalvoice.cliente import Cliente

cliente = Cliente("SEU_TOKEN", 'HOST') #ex: api.totalvoice.com.br

#Cria TTS
numero_destino = "48999999999"
mensagem = "Olá, esta mensagem será lida"
response = cliente.tts.enviar(numero_destino, mensagem)
print(response)

#Get TTS
id = "1958"
response = cliente.tts.get_by_id(id)
print(response)

#Relatório de TTS
data_inicio = "2016-03-30T17:15:59-03:00"
data_fim = "2016-03-30T17:15:59-03:00"
response = cliente.tts.get_relatorio(data_inicio, data_fim)
print(response)

```

### Conferência
Módulo responsável por criação de Conferências.

```python
from totalvoice.cliente import Cliente

cliente = Cliente("SEU_TOKEN", 'HOST') #ex: api.totalvoice.com.br

#Cria conferência
response = cliente.conferencia.cria_conferencia()
print(response)

#Get conferência
id = "1958"
response = cliente.conferencia.get_by_id(id)
print(response)

#Add número na conferência
id_conferencia = "15"
numero = "48999999999"
response = cliente.conferencia.add_numero_conferencia(id_conferencia, numero)
print(response)

```


## Licença

MIT
