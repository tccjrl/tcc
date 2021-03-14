var endpoint = 'api/data'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        data = Object.values(data)
        setChart(data[0])
    },
    error: function(error_data){
        console.log("error")
    }
})

function setChart(lista_hosts) {
    for (let host of lista_hosts) {
        host = Object.values(host)

        //cria uma div para cada host e adiciona no dashboard
        var divHost = document.createElement('div')
        divHost.setAttribute('id', host[0])
        var pnomeHost = document.createElement('p')
        var nomeHost = document.createTextNode(host[0])
        pnomeHost.appendChild(nomeHost)

        pnomeHost.style.textAlign = "center"
        pnomeHost.style.fontSize = "30px"
        pnomeHost.style.color = "white"
        pnomeHost.style.backgroundColor = "rgba(16,16,16,.5)"

        divHost.appendChild(pnomeHost)
        var dashboard = document.getElementById('dashboard')
        dashboard.appendChild(divHost)

        //cria as divs dentro das divs do host
        createDivItens(host)

        //adiciona espaço
        var br = document.createElement('br')
        dashboard.appendChild(br)
    }
}

//cria as divs dentro das divs do host
function createDivItens(host){
    var nomeHost = host[0]
    var canvas = "canvas"
    for (let item of host[1]) {
        var divItem = document.createElement('div')
        divItem.setAttribute('id', nomeHost + "+" + item['item_nome'])

        divItem.style.borderStyle = "groove"

        var pNomeItem = document.createElement('p')
        var nomeItem = document.createTextNode(item['item_nome'])
        pNomeItem.appendChild(nomeItem)

        pNomeItem.style.textAlign = "center"
        pNomeItem.style.fontSize = "20px"

        divItem.appendChild(pNomeItem)
        var br = document.createElement('br')
        divItem.appendChild(br)

        //Se o item for do tipo Numérico gera o elemento canvas para o gráfico
        if ((item['item_tipoInformacao'] == "NI") || (item['item_tipoInformacao'] == "ND")) {
            var canvasItem = document.createElement('canvas')
            canvasItem.setAttribute('id', canvas + "+" + nomeHost + "+" + item['item_nome'])
            divItem.appendChild(canvasItem)
        }

        var host = document.getElementById(nomeHost)
        host.appendChild(divItem)

        //Se o item for do tipo Numérico gera o gráfico dentro do canvas
        if ((item['item_tipoInformacao'] == "NI") || (item['item_tipoInformacao'] == "ND")) {
            criaChart(nomeHost, item)
        }

        //Se o item for do tipo Caracter chama a função para criar o elemento texto dentro da div
        if ((item['item_tipoInformacao'] == "CH")) {
            criaCharData(nomeHost, item)
        }

        //Se o item for do tipo log chama a função para criar o elemento texto dentro da div
        if ((item['item_tipoInformacao'] == "LG")) {
            criaLogData(nomeHost, item)
        }
    }
}

//cria o grafico
function criaChart(nomeHost, item){
    console.log(item['labels'])
    var nomeItem = item['item_nome']
    var canvas = "canvas"
    var ctx = document.getElementById(canvas + "+" + nomeHost + "+" + nomeItem)
    labels = formatTimeLabel(item['labels'])

    //Para itens do tipo: Numérico inteiro
    if (item['item_tipoInformacao'] == "NI") {
            //Type, Data e options
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: nomeItem,
                    data: item['data'],
                    borderColor: 'green',
                    backgroundColor: 'green',
                }]
            }
        })
    }

    //Para itens do tipo: Numérico Decimal
    if (item['item_tipoInformacao'] == "ND") {
        //Type, Data e options
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: item['labels'],
                datasets: [{
                    label: nomeItem,
                    data: item['data'],
                    borderColor: 'green',
                    backgroundColor: 'green',
                }]
            }
        })
    }
}

//cria elemento de caracter
function criaCharData (nomeHost, Item){

    var ct = -1
    var labels = formatTimeLabel(Item['labels'])
    var divItem = document.getElementById(nomeHost + "+" + Item['item_nome'])
    var textArea = document.createElement('p')
    var atualizao = document.createElement('p')

    atualizao.style.textAlign = 'right'

    var space = document.createElement('br')

    textArea.style.textAlign = "center"
    textArea.style.fontSize = "25px"

    for (let data of Item['data']){
        ct = ct + 1
    }


    var textNode = document.createTextNode(Item['data'][ct])
    var textNodeAtualicao = document.createTextNode('Última atualização: ' + labels[ct])

    atualizao.appendChild(textNodeAtualicao)
    textArea.appendChild(textNode)
    divItem.appendChild(textArea)
    divItem.appendChild(space)
    divItem.appendChild(atualizao)
}

//cria elemento de log
function criaLogData (nomeHost, Item){

    /*var ct = 0
    var divItem = document.getElementById(nomeHost + "+" + Item['item_nome'])
    var str = ''

    for (let label of formatTimeLabel(Item['labels'])) {
        str = label + ' : ' + Item['data'][ct]
        var logP = document.createElement('p')
        var logTextNode = document.createTextNode(str)
        logP.appendChild(logTextNode)
        divItem.appendChild(logP)
        ct = ct + 1
    }*/

    var ct = 0
    var divItem = document.getElementById(nomeHost + "+" + Item['item_nome'])
    var textArea = document.createElement('textarea')
    var str = ''

    for (let label of formatTimeLabel(Item['labels'])) {
        str = label + ' : ' + Item['data'][ct] + "\n"
        var logTextNode = document.createTextNode(str)
        textArea.appendChild(logTextNode)
        textArea.style.width = '50%'
        textArea.style.height = '100px'
        textArea.style.position = 'relative'
        textArea.style.left = '25%'

        divItem.appendChild(textArea)
    }
}


//formata os labels dos horários dos gráficos
function formatTimeLabel (listLabel) {
    var formatedListLabel = []

    for (let label of listLabel) {
        formatedListLabel.push(label.split('.')[0])
    }

    return formatedListLabel
}