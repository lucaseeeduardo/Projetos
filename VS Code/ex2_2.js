const frm = document.querySelector("form") // aqui o programa seleciona meio que uma "array" chamada form 
const resp1 = document.querySelector("h3") // aqui o programa diz que resp1 está dentro da header 3
const resp2 = document.querySelector("h4") // aqui o programa diz que a resp2 está dentro da header 4

frm.addEventListener("submit", (e) => {
    const título = frm.inTítulo.value // aqui eu aloco na variável "título" o frm.titulo como se fosse uma struct e obtenho o conteúdo de value
    const duração = Number(frm.inDuração.value) // alocando em "duração" o conteúdo do id duração
    const horas = Math.floor(duração/60) // math.floor usa só a parte inteira do número, se a duraçãofor 240-> 245/60 = 4,08 -> horas = 4
    const minutos = duração % 60 // resto de duração (pra saber os minutos) resto de 245/60 = 5, 

    resp1.innerText= título
    resp2.innerText= `Durou ${horas}horas e ${minutos}minutos`
    e.preventDefault()

})