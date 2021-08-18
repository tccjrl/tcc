var endpoint = 'api/data'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        data = Object.values(data)
        setDataTimeNow()
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
    //console.log(item['labels'])
    var nomeItem = item['item_nome']
    var canvas = "canvas"
    var ctx = document.getElementById(canvas + "+" + nomeHost + "+" + nomeItem)
    labels = formatTimeLabel(item['labels'])
    info = dateFilter(labels, item['data'])


    //array de cores vazio
    colors = [];

    //verifica se data é número ou inválido
    for (i = 0; i < info['datasFiltered'].length; i++){
        if (!isNaN(Number(info['datasFiltered'][i]))){
            colors[i] = 'green'
        }
        else{
            info['datasFiltered'][i] = 0
            colors[i] = 'red'
        }
    }

    //Para itens do tipo: Numérico inteiro
    if (item['item_tipoInformacao'] == "NI") {
            //Type, Data e options
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: info['labelsFiltered'],
                datasets: [{
                    label: nomeItem,
                    data: info['datasFiltered'],
                    borderWidth: 6,
                    borderColor: colors,
                    backgroundColor: 'rgba(126,232,85,0.45)',
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
                labels: info['labelsFiltered'],
                datasets: [{
                    label: nomeItem,
                    data: info['datasFiltered'],
                    borderWidth: 6,
                    borderColor: colors,
                    backgroundColor: 'green',
                }]
            }
        })
    }
}

//cria elemento de caracter
function criaCharData (nomeHost, Item){

    var info = dateFilter(Item['labels'], Item['data'])
    //console.log(info)

    var ct = -1
    var labels = info['labelsFiltered']
    var divItem = document.getElementById(nomeHost + "+" + Item['item_nome'])
    var textArea = document.createElement('p')
    var atualizao = document.createElement('p')

    atualizao.style.textAlign = 'right'

    var space = document.createElement('br')

    textArea.style.textAlign = "center"
    textArea.style.fontSize = "25px"

    for (let data of info['datasFiltered']){
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

    var info = dateFilter(Item['labels'], Item['data'])

    for (let label of info['labelsFiltered']) {
        str = label + ' : ' + info['datasFiltered'][ct] + "\n"
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

//Seta data inicial e final assim que abre a página
function setDataTimeNow(){
    //formato para set no imput datatime-local: 2017-06-13T13:00

    //Data inicial
    var initDate = new Date();
    initDate.setHours(initDate.getHours() - 1); // diminui uma hora
    var initDay = String(initDate.getDate()).padStart(2, '0');
    var initMonth = String(initDate.getMonth() + 1).padStart(2, '0');
    var initYear = initDate.getFullYear();
    var initHour = String(initDate.getHours()).padStart(2, '0');
    var initMinute = String(initDate.getMinutes()).padStart(2, '0');
    var initDateFmtd = initYear + '-' + initMonth + '-' + initDay + 'T' + initHour + ':' + initMinute;
    var dateTimeInit = document.getElementById('initDateTimeInput').value = initDateFmtd
    //console.log(initDateFmtd)

    //Data final
    var finalDate = new Date();
    var finalDay = String(finalDate.getDate()).padStart(2, '0');
    var finalMonth = String(finalDate.getMonth() + 1).padStart(2, '0');
    var finalYear = finalDate.getFullYear();
    var finalHour = String(finalDate.getHours()).padStart(2, '0');
    var finalMinute = String(finalDate.getMinutes()).padStart(2, '0');
    var finalDateFmtd = finalYear + '-' + finalMonth + '-' + finalDay + 'T' + finalHour + ':' + finalMinute;
    var dateTimeFinal = document.getElementById('finalDateTimeInput').value = finalDateFmtd
    //console.log(finalDateFmtd)
}

function dateFilter(labels, datas){

    var dateTimeInit = document.getElementById('initDateTimeInput').value
    //console.log(dateTimeInit)
    var initDate = new Date()
    initDate.setFullYear(dateTimeInit.substr(0,4))
    initDate.setMonth(parseInt(dateTimeInit.substr(5, 2))-1)
    initDate.setDate(dateTimeInit.substr(8, 2))
    initDate.setHours(dateTimeInit.substr(11, 2))
    initDate.setMinutes(dateTimeInit.substr(14, 2))
    //console.log(initDate)

    var dateTimeFinal = document.getElementById('finalDateTimeInput').value
    var finalDate = new Date()
    finalDate.setFullYear(dateTimeFinal.substr(0,4))
    finalDate.setMonth(parseInt(dateTimeFinal.substr(5, 2))-1)
    finalDate.setDate(dateTimeFinal.substr(8, 2))
    finalDate.setHours(dateTimeFinal.substr(11, 2))
    finalDate.setMinutes(dateTimeFinal.substr(14, 2))

    listDates = []

    for (let date of labels){

        var objDate = new Date()
        objDate.setFullYear(date.substr(0,4))
        objDate.setMonth(parseInt(date.substr(5, 2))-1)
        //console.log(date.substr(5, 2))
        objDate.setDate(date.substr(8, 2))
        objDate.setHours(date.substr(11, 2))
        objDate.setMinutes(date.substr(14, 2))
        //console.log(date)
        //console.log(objDate)
        listDates.push(objDate)
    }


    labelsFiltered = []
    datasFiltered = []
    ct = 0
    //2021-08-16 21:03:18

    for (let date of listDates){
        if ((date >= initDate) && (date <= finalDate)){
            var day = String(date.getDate()).padStart(2, '0');
            var month = String(date.getMonth() + 1).padStart(2, '0');
            var year = date.getFullYear();
            var hour = String(date.getHours()).padStart(2, '0');
            var minute = String(date.getMinutes()).padStart(2, '0');
            labelsFiltered.push(year + '-' + month + '-' + day + ' ' + hour + ':' + minute)
            datasFiltered.push(datas[ct])
        }
        ct = ct + 1
    }
    ct = 0
    return {
        labelsFiltered: labelsFiltered,
        datasFiltered: datasFiltered
    }
}

function buttonFilterDate(){

    document.getElementById('dashboard').innerHTML = '';


    $.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        data = Object.values(data)
        //setDataTimeNow()
        setChart(data[0])
    },
    error: function(error_data){
        console.log("error")
    }
})
}